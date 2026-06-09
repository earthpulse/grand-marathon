# Main feature extraction script for wildfire hazard model - designed for evaluability and clarity
# The script extracts time-aligned NDVI and t2m features from remote sensing/satellite sources for wildfire hotspots in Galicia, 2025.
# For every hotspot (fire detection) we prepare a "positive" example (time/location of actual fire)
# For every positive, we generate a "negative" example: same location, but a date one month offset, guaranteeing no fire label
# For every sample, we extract:
#   - NDVI (Normalized Difference Vegetation Index) from Sentinel-2 in a time window before the fire/neg date
#   - Past 5 daily t2m (2m air temperature) values from ERA5 reanalysis

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if present

import random

import geopandas as gpd
from spai.data.satellite import load_satellite_imagery
from tqdm import tqdm
from shapely.geometry import box, Point
import pandas as pd
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from dateutil.relativedelta import relativedelta

from utils import load_era5  # Utility function for downloading/caching ERA5 data

# Constants controlling sample lookbacks and locations of files
NEGATIVE_DATE_WINDOW_DAYS = 5  # Days window for negative NDVI search
POSITIVE_IMAGE_LOOKBACK_DAYS = (
    5  # Max days to look back before fire for a positive NDVI
)
T2M_LOOKBACK_DAYS = 5  # Number of days prior to event for daily t2m sequence
SAMPLE_LIMIT = (
    None  # Optional: cap number of hotspots to process for fast experimentation
)
PATH = "../data"  # Data root directory


def negative_sample_date(acq_date):
    """
    Pick a feature date one month before/after, staying within the ERA5 year.
    Ensures negative samples do not leak over year boundaries.
    """
    acq_date = pd.Timestamp(acq_date)
    if acq_date.month == 1:
        return acq_date + relativedelta(months=1)
    if acq_date.month == 12:
        return acq_date - relativedelta(months=1)
    if random.random() < 0.5:
        return acq_date - relativedelta(months=1)
    return acq_date + relativedelta(months=1)


def process_hotspot(args):
    """
    Extract NDVI for one hotspot/negative sample (location/date).
    Args are (date, lon, lat, label, acq_date).
    If label==1 (positive), extract NDVI up to 5 days before fire.
    If label==0 (negative), extract NDVI within ±5 days of sample date.
    Returns NDVI and metadata if successful, else None.
    """
    _, lon, lat, label, acq_date = args
    acq_date = pd.Timestamp(acq_date)
    try:
        # Define 2km x 2km bounding box around the point for imagery extraction
        bb = box(lon - 0.001, lat - 0.001, lon + 0.001, lat + 0.001)
        if label == 1:
            # For positives: exclude fire day, use max 5-day lookback, last valid NDVI is day before fire
            search_start = acq_date - timedelta(days=POSITIVE_IMAGE_LOOKBACK_DAYS)
            search_end = acq_date
            target_date = acq_date - timedelta(days=1)
            last_valid_date = target_date
        else:
            # For negatives: sample date is synthetic, ±5d search window
            target_date = pd.Timestamp(args[0])
            search_start = target_date - timedelta(days=NEGATIVE_DATE_WINDOW_DAYS)
            search_end = target_date + timedelta(days=NEGATIVE_DATE_WINDOW_DAYS)

        # Query Sentinel-2 NDVI for the time window and bounding box
        data = load_satellite_imagery(
            date=[search_start, search_end],
            aoi=bb,
            collection="sentinel-2-l2a",
        )
        if data is not None and data.sizes.get("time", 0) > 0:
            # Pick the snapshot closest in time to our event/target
            snapshot = data.sel(time=target_date, method="nearest")
            image_date = pd.Timestamp(snapshot.time.values).normalize()
            # Validity check: Ensure snapshot falls inside intended window
            if label == 1:
                if (
                    image_date < search_start.normalize()
                    or image_date > last_valid_date.normalize()
                ):
                    return None
            elif (
                abs((image_date - target_date.normalize()).days)
                > NEGATIVE_DATE_WINDOW_DAYS
            ):
                return None

            # Compute NDVI: (NIR - Red) / (NIR + Red)
            red = snapshot.red
            nir = snapshot.nir
            ndvi = (nir - red) / (nir + red)
            value = ndvi.sel(longitude=lon, latitude=lat, method="nearest").values
            return {
                "date": image_date,  # Date of acquired satellite image (may not exactly match target)
                "ndvi": float(value),  # The NDVI value for this point/date
                "lon": lon,
                "lat": lat,
                "label": label,  # 1 for positive (fire) sample, 0 for negative (no fire)
                "acq_date": acq_date,  # The acquisition date of the hotspot (fire day)
            }
    except Exception:
        # Robustness: fail silently if extraction fails for this sample (cloud, missing data, etc.)
        return None


def lookup_t2m_series(t2m_daily, acq_date, lon, lat, days=T2M_LOOKBACK_DAYS):
    """
    For a point (lon/lat) and a given date, extract daily mean t2m for the previous N days (not including acq_date).
    Returns a sequence [t2m_-N, ..., t2m_-1].
    """
    acq_date = pd.Timestamp(acq_date)
    return [
        float(
            t2m_daily.sel(
                valid_time=acq_date - timedelta(days=offset),
                longitude=lon,
                latitude=lat,
                method="nearest",
            ).values
        )
        for offset in range(days, 0, -1)
    ]


def main():
    # === 1. Load all active fire "hotspots" for the region ===
    print("Loading hotspots...", end="", flush=True)
    hotspots = gpd.read_file(f"{PATH}/NW_Spain_2025_VIIRS_hotspots.geojson")
    print("done")

    # === 2. Download or load pre-cached ERA5 weather data for region/year ===
    print("Loading era5...", end="", flush=True)
    era5 = load_era5(
        aoi=gpd.GeoDataFrame(geometry=[box(*hotspots.total_bounds)], crs=hotspots.crs),
        start_date="2025-01-01",
        end_date="2025-12-31",
        dataset="reanalysis-era5-single-levels-v0",
        era5_vars=["t2m"],
    )
    print("done")

    # === 3. Compute daily mean t2m grid for each day (reduces to one t2m per day/pixel) ===
    print("Accumulating daily t2m...", end="", flush=True)
    t2m_daily = era5["t2m"].groupby(era5.valid_time.dt.floor("D")).mean("valid_time")
    t2m_daily = t2m_daily[:-1, :, :]  # Remove final (possibly incomplete) day
    t2m_daily = t2m_daily.rename({"floor": "valid_time"}).compute()
    print("done")

    # === 4. Limit to first N hotspots for dev/testing, if SAMPLE_LIMIT set ===
    hotspots_subset = hotspots if SAMPLE_LIMIT is None else hotspots[:SAMPLE_LIMIT]
    print(
        f"Processing {len(hotspots_subset)} hotspots"
        + ("" if SAMPLE_LIMIT is None else f" (limit={SAMPLE_LIMIT})")
        + "...",
        flush=True,
    )

    # === 5. Create positive tasks: (fire-acq_date, lon, lat, label=1, acq_date) for each observed hotspot ===
    positive_tasks = [
        (
            row["ACQ_DATE"],
            row.geometry.centroid.x,
            row.geometry.centroid.y,
            1,
            row["ACQ_DATE"],
        )
        for _, row in hotspots_subset.iterrows()
    ]

    # === 6. Allocate feature table for results (ndvi/t2m/label per sample) ===
    table = {
        "date": [],
        "acq_date": [],
        "ndvi": [],
        "hotspot": [],
        **{f"t2m_{i}": [] for i in range(1, T2M_LOOKBACK_DAYS + 1)},
        "label": [],
    }

    def append_result(res):
        """
        Helper to add a processed sample's features to the table.
        Looks up t2m sequence for each sample on the fly.
        """
        table["date"].append(res["date"])
        table["acq_date"].append(res["acq_date"])
        table["ndvi"].append(res["ndvi"])
        table["hotspot"].append(Point(res["lon"], res["lat"]))
        t2m_series = lookup_t2m_series(
            t2m_daily, res["acq_date"], res["lon"], res["lat"]
        )
        for i, value in enumerate(t2m_series, start=1):
            table[f"t2m_{i}"].append(value)
        table["label"].append(res["label"])

    successful_hotspots = []  # To record only those positive samples for which feature extraction succeeded

    # === 7. Extract features for all positive (fire) hotspot samples in parallel ===
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_hotspot, task): task for task in positive_tasks
        }
        # Use tqdm progress bar for transparency/evaluation
        for future in tqdm(as_completed(futures), total=len(futures), desc="Positives"):
            res = future.result()
            if res is not None:
                append_result(res)
                # Record successful fire sample locations, so negatives can match same points (avoid missing data bias)
                successful_hotspots.append((res["acq_date"], res["lon"], res["lat"]))

    # === 8. Prepare negative (no-fire) tasks: pick dates one month before/after per successful positive ===
    negative_tasks = []
    for acq_date, lon, lat in successful_hotspots:
        neg_date = negative_sample_date(acq_date)
        negative_tasks.append((neg_date, lon, lat, 0, acq_date))  # label=0

    # === 9. Extract features for all negative samples in parallel ===
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_hotspot, task): task for task in negative_tasks
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Negatives"):
            res = future.result()
            if res is not None:
                append_result(res)

    # === 10. Export the tabular feature data (date, NDVI, t2m_1...5, label, etc) ===
    t2m_columns = [f"t2m_{i}" for i in range(1, T2M_LOOKBACK_DAYS + 1)]
    data = pd.DataFrame(
        table,
        columns=["date", "acq_date", "ndvi", "hotspot", *t2m_columns, "label"],
    )
    # (Optional) Re-index, sort by date for easy review
    data = data.set_index("date").sort_index()
    # Save to CSV for model training, benchmarks, or validation
    data.to_csv(f"{PATH}/features.csv", index=False)


if __name__ == "__main__":
    main()
