"""
Rule-based operational priority for wildfire response.

Dimensions (hazard, exposure, vulnerability) are classified ordinally, then
combined through a lookup table — not multiplied as a continuous risk score.
"""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

try:
    import rasterio
    from pyproj import Geod
except ImportError:  # pragma: no cover
    rasterio = None
    Geod = None

RULE_SET_ID = "rule_based_v1"
_GEOD = Geod(ellps="WGS84") if Geod is not None else None

_HAZARD_PCT_KEYS = {1: "hazard_pct_low", 2: "hazard_pct_medium", 3: "hazard_pct_high", 4: "hazard_pct_critical"}
_PRIORITY_PCT_KEYS = {
    1: "priority_pct_low",
    2: "priority_pct_medium",
    3: "priority_pct_high",
    4: "priority_pct_critical",
}

# Ordinal dimension classes (hazard / exposure / vulnerability)
DIMENSION_LABELS = {
    0: "No data",
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Critical",
}

# Operational priority output
PRIORITY_LABELS = {
    0: "No data",
    1: "Low Priority",
    2: "Medium Priority",
    3: "High Priority",
    4: "Critical Priority",
}

# Continuous [0, 1] → dimension class (plan thresholds)
DIMENSION_THRESHOLDS: list[tuple[float, float, int]] = [
    (0.00, 0.25, 1),
    (0.25, 0.50, 2),
    (0.50, 0.75, 3),
    (0.75, 1.01, 4),
]

# Documented rule rows (h_min, e_min, v_min, priority) — first match when building LUT
PRIORITY_RULES: list[dict] = [
    {
        "priority": 4,
        "label": "Critical",
        "hazard_min": 3,
        "exposure_min": 3,
        "vulnerability_min": 3,
        "note": "All dimensions High or Critical",
    },
    {
        "priority": 4,
        "label": "Critical",
        "hazard_eq": 4,
        "exposure_min": 2,
        "vulnerability_min": 2,
        "note": "Critical hazard + Medium+ exposure and vulnerability",
    },
    {
        "priority": 3,
        "label": "High",
        "hazard_min": 3,
        "exposure_min": 3,
        "note": "High/Critical hazard + High exposure",
    },
    {
        "priority": 3,
        "label": "High",
        "hazard_min": 3,
        "vulnerability_min": 3,
        "note": "High/Critical hazard + High vulnerability",
    },
    {
        "priority": 3,
        "label": "High",
        "hazard_eq": 2,
        "exposure_min": 3,
        "vulnerability_min": 3,
        "note": "Medium hazard + High exposure + High vulnerability",
    },
    {
        "priority": 2,
        "label": "Medium",
        "hazard_min": 2,
        "either_exp_or_vuln": True,
        "note": "Medium+ hazard and Medium+ exposure OR vulnerability",
    },
    {
        "priority": 1,
        "label": "Low",
        "catch_all": True,
        "note": "All remaining valid combinations",
    },
]


def classify_dimension(values: np.ndarray) -> np.ndarray:
    """Map continuous [0, 1] raster to ordinal classes 0–4."""
    out = np.zeros(values.shape, dtype=np.uint8)
    valid = np.isfinite(values)
    for lo, hi, cls in DIMENSION_THRESHOLDS:
        out[valid & (values >= lo) & (values < hi)] = cls
    return out


def _rule_matches(h: int, e: int, v: int, rule: dict) -> bool:
    if rule.get("catch_all"):
        return h > 0 and e > 0 and v > 0

    if h == 0 or e == 0 or v == 0:
        return False

    if "hazard_eq" in rule and h != rule["hazard_eq"]:
        return False
    if "hazard_min" in rule and h < rule["hazard_min"]:
        return False
    if "exposure_min" in rule and e < rule["exposure_min"]:
        return False
    if "vulnerability_min" in rule and v < rule["vulnerability_min"]:
        return False

    if rule.get("either_exp_or_vuln"):
        return e >= 2 or v >= 2

    return True


def priority_from_classes(h: int, e: int, v: int) -> int:
    """Apply rules in priority order (Critical → Low)."""
    if h == 0 or e == 0 or v == 0:
        return 0

    for rule in PRIORITY_RULES:
        if _rule_matches(h, e, v, rule):
            return rule["priority"]

    return 1


def build_priority_lut() -> np.ndarray:
    """5×5×5 lookup table indexed by (hazard, exposure, vulnerability) class."""
    lut = np.zeros((5, 5, 5), dtype=np.uint8)
    for h in range(5):
        for e in range(5):
            for v in range(5):
                lut[h, e, v] = priority_from_classes(h, e, v)
    return lut


def apply_priority_lut(
    hazard_cls: np.ndarray,
    exposure_cls: np.ndarray,
    vulnerability_cls: np.ndarray,
    lut: np.ndarray,
) -> np.ndarray:
    """Vectorised priority from three class rasters."""
    return lut[hazard_cls, exposure_cls, vulnerability_cls]


def explain_priority(h: int, e: int, v: int, priority: int) -> str:
    """Human-readable explanation for one (h, e, v, priority) tuple."""
    if priority == 0:
        return "No operational priority — missing hazard, exposure or vulnerability data."

    p = PRIORITY_LABELS[priority]

    if priority == 4:
        if h >= 3 and e >= 3 and v >= 3:
            return (
                f"{p} because hazard, exposure and vulnerability are all "
                f"{DIMENSION_LABELS[min(h, 4)].lower()} or higher."
            )
        return (
            f"{p} because critical fire-prone conditions coincide with "
            f"populated and vulnerable areas."
        )

    if priority == 3:
        if h >= 3 and e >= 3:
            return f"{p} because hazard and exposure are {DIMENSION_LABELS[e].lower()}."
        if h >= 3 and v >= 3:
            return (
                f"{p} because hazard is {DIMENSION_LABELS[h].lower()} and "
                f"vulnerable communities may be affected."
            )
        return f"{p} because elevated hazard coincides with significant exposure and vulnerability."

    if priority == 2:
        return f"{p} because elevated fire conditions coincide with moderate exposure or vulnerability."

    return f"{p} because operational relevance is limited."


def pixel_area_km2_at(transform, row: int, col: int) -> float:
    """Approximate geodesic cell area (km²) at one grid position."""
    if rasterio is None or _GEOD is None:
        raise ImportError("rasterio and pyproj are required for area calculations")
    x, y = rasterio.transform.xy(transform, row, col, offset="center")
    x2, y2 = rasterio.transform.xy(transform, row, col + 1, offset="center")
    x3, y3 = rasterio.transform.xy(transform, row + 1, col, offset="center")
    _, _, w = _GEOD.inv(x, y, x2, y2)
    _, _, h = _GEOD.inv(x, y, x3, y3)
    return abs(w * h) / 1e6


def _pct_by_class(arr: np.ndarray, mask: np.ndarray, class_keys: dict[int, str]) -> dict[str, float]:
    n = int(mask.sum())
    if n == 0:
        return {key: 0.0 for key in class_keys.values()}
    return {class_keys[c]: round(100.0 * ((arr == c) & mask).sum() / n, 4) for c in class_keys}


def _build_summary(
    hazard_pct: dict[str, float],
    priority_pct: dict[str, float],
    means: dict[str, float],
    diagnostics: dict[str, float],
) -> str:
    high_hazard = hazard_pct.get("hazard_pct_high", 0) + hazard_pct.get("hazard_pct_critical", 0)
    high_priority = priority_pct.get("priority_pct_high", 0) + priority_pct.get("priority_pct_critical", 0)
    gap = diagnostics.get("diag_pct_high_hazard_low_priority", 0)

    if gap > 20 and means.get("mean_exposure", 0) < 0.1:
        return (
            "Elevated hazard over much of the modeled area; operational priority remains "
            "mostly low due to limited exposure."
        )
    if high_priority > 5:
        return "Significant areas warrant elevated operational attention."
    if high_hazard > 40 and high_priority < 5:
        return (
            "Wildfire hazard is widespread, but operational priority stays low where "
            "exposure and vulnerability are limited."
        )
    return "Operational priority is predominantly low across the modeled area."


def build_daily_analytics(
    analysis_date: str,
    hazard: np.ndarray,
    hazard_cls: np.ndarray,
    priority: np.ndarray,
    exposure_cont: np.ndarray,
    vulnerability_cont: np.ndarray,
    transform,
    aoi_id: str = "seadur",
    analysis_mask: np.ndarray | None = None,
) -> dict:
    """
    Flat daily summary dict for JSON export (one row per date in pandas).

    Percentages use pixels with hazard_class > 0 (optionally clipped to analysis_mask).
    """
    modeled = hazard_cls > 0
    mask = modeled & analysis_mask if analysis_mask is not None else modeled
    n = int(mask.sum())

    hazard_pct = _pct_by_class(hazard_cls, mask, _HAZARD_PCT_KEYS)
    priority_pct = _pct_by_class(priority, mask, _PRIORITY_PCT_KEYS)

    if n > 0:
        means = {
            "mean_hazard": round(float(np.nanmean(hazard[mask])), 6),
            "mean_exposure": round(float(np.nanmean(exposure_cont[mask])), 6),
            "mean_vulnerability": round(float(np.nanmean(vulnerability_cont[mask])), 6),
        }
        max_hazard_class = int(hazard_cls[mask].max())
        max_operational_priority_class = int(priority[mask].max())
        high_hazard = mask & (hazard_cls >= 3)
        high_priority = mask & (priority >= 3)
        gap = mask & (hazard_cls >= 3) & (priority <= 1)
        diagnostics = {
            "diag_pct_high_or_critical_hazard": round(100.0 * high_hazard.sum() / n, 4),
            "diag_pct_high_or_critical_priority": round(100.0 * high_priority.sum() / n, 4),
            "diag_pct_high_hazard_low_priority": round(100.0 * gap.sum() / n, 4),
        }
        row, col = hazard.shape[0] // 2, hazard.shape[1] // 2
        modeled_area_km2 = round(pixel_area_km2_at(transform, row, col) * n, 2)
    else:
        means = {"mean_hazard": None, "mean_exposure": None, "mean_vulnerability": None}
        max_hazard_class = 0
        max_operational_priority_class = 0
        diagnostics = {
            "diag_pct_high_or_critical_hazard": 0.0,
            "diag_pct_high_or_critical_priority": 0.0,
            "diag_pct_high_hazard_low_priority": 0.0,
        }
        modeled_area_km2 = 0.0

    summary = _build_summary(hazard_pct, priority_pct, means, diagnostics)

    return {
        "analysis_date": analysis_date,
        "aoi": aoi_id,
        "rule_set": RULE_SET_ID,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "modeled_pixel_count": n,
        "modeled_area_km2": modeled_area_km2,
        **hazard_pct,
        **priority_pct,
        **means,
        "max_hazard_class": max_hazard_class,
        "max_operational_priority_class": max_operational_priority_class,
        **diagnostics,
        "summary": summary,
    }
