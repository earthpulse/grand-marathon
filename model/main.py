# for each hotspot
# get ndvi in a max window of 5 days before
# get daily accumulated t2m for 5 days before (time series)
# generate a negative sample by picking a date one month before/after, staying within the ERA5 year


from dotenv import load_dotenv

load_dotenv()

import random

import geopandas as gpd
from spai.data.satellite import load_satellite_imagery
from tqdm import tqdm
from shapely.geometry import box, Point
import pandas as pd
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from dateutil.relativedelta import relativedelta

from utils import load_era5  # spai need some updates

NEGATIVE_DATE_WINDOW_DAYS = 5
POSITIVE_IMAGE_LOOKBACK_DAYS = 5
T2M_LOOKBACK_DAYS = 5
SAMPLE_LIMIT = None  # 1000  # set to None to process all hotspots
PATH = "../data"


def negative_sample_date(acq_date):
    """Pick a feature date one month before/after, staying within the ERA5 year."""
    acq_date = pd.Timestamp(acq_date)
    if acq_date.month == 1:
        return acq_date + relativedelta(months=1)
    if acq_date.month == 12:
        return acq_date - relativedelta(months=1)
    if random.random() < 0.5:
        return acq_date - relativedelta(months=1)
    return acq_date + relativedelta(months=1)


def process_hotspot(args):
    """Fetch NDVI for one hotspot. Takes plain (date, lon, lat, label, acq_date)."""
    _, lon, lat, label, acq_date = args
    acq_date = pd.Timestamp(acq_date)
    try:
        bb = box(lon - 0.001, lat - 0.001, lon + 0.001, lat + 0.001)
        if label == 1:
            # ACQ_DATE is one day after the event; imagery loader excludes the end date.
            search_start = acq_date - timedelta(days=POSITIVE_IMAGE_LOOKBACK_DAYS)
            search_end = acq_date
            target_date = acq_date - timedelta(days=1)
            last_valid_date = target_date
        else:
            target_date = pd.Timestamp(args[0])
            search_start = target_date - timedelta(days=NEGATIVE_DATE_WINDOW_DAYS)
            search_end = target_date + timedelta(days=NEGATIVE_DATE_WINDOW_DAYS)

        data = load_satellite_imagery(
            date=[search_start, search_end],
            aoi=bb,
            collection="sentinel-2-l2a",
        )
        if data is not None and data.sizes.get("time", 0) > 0:
            snapshot = data.sel(time=target_date, method="nearest")
            image_date = pd.Timestamp(snapshot.time.values).normalize()
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

            red = snapshot.red
            nir = snapshot.nir
            ndvi = (nir - red) / (nir + red)
            value = ndvi.sel(longitude=lon, latitude=lat, method="nearest").values
            return {
                "date": image_date,
                "ndvi": float(value),
                "lon": lon,
                "lat": lat,
                "label": label,
                "acq_date": acq_date,
            }
    except Exception:
        return None


def lookup_t2m_series(t2m_daily, acq_date, lon, lat, days=T2M_LOOKBACK_DAYS):
    """Daily t2m for the `days` before acquisition (acq-5 .. acq-1)."""
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
    print("Loading hotspots...", end="", flush=True)
    hotspots = gpd.read_file(f"{PATH}/NW_Spain_2025_VIIRS_hotspots.geojson")
    print("done")

    print("Loading era5...", end="", flush=True)
    era5 = load_era5(
        aoi=gpd.GeoDataFrame(geometry=[box(*hotspots.total_bounds)], crs=hotspots.crs),
        start_date="2025-01-01",
        end_date="2025-12-31",
        dataset="reanalysis-era5-single-levels-v0",
        era5_vars=["t2m"],
    )
    print("done")

    print("Accumulating daily t2m...", end="", flush=True)
    t2m_daily = era5["t2m"].groupby(era5.valid_time.dt.floor("D")).mean("valid_time")
    t2m_daily = t2m_daily[:-1, :, :]
    t2m_daily = t2m_daily.rename({"floor": "valid_time"}).compute()
    print("done")

    hotspots_subset = hotspots if SAMPLE_LIMIT is None else hotspots[:SAMPLE_LIMIT]
    print(
        f"Processing {len(hotspots_subset)} hotspots"
        + ("" if SAMPLE_LIMIT is None else f" (limit={SAMPLE_LIMIT})")
        + "...",
        flush=True,
    )
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

    table = {
        "date": [],
        "acq_date": [],
        "ndvi": [],
        "hotspot": [],
        **{f"t2m_{i}": [] for i in range(1, T2M_LOOKBACK_DAYS + 1)},
        "label": [],
    }

    def append_result(res):
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

    successful_hotspots = []

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_hotspot, task): task for task in positive_tasks
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Positives"):
            res = future.result()
            if res is not None:
                append_result(res)
                successful_hotspots.append((res["acq_date"], res["lon"], res["lat"]))

    negative_tasks = []
    for acq_date, lon, lat in successful_hotspots:
        neg_date = negative_sample_date(acq_date)
        negative_tasks.append((neg_date, lon, lat, 0, acq_date))

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_hotspot, task): task for task in negative_tasks
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Negatives"):
            res = future.result()
            if res is not None:
                append_result(res)

    t2m_columns = [f"t2m_{i}" for i in range(1, T2M_LOOKBACK_DAYS + 1)]
    data = pd.DataFrame(
        table,
        columns=["date", "acq_date", "ndvi", "hotspot", *t2m_columns, "label"],
    )
    data = data.set_index("date").sort_index()
    data.to_csv(f"{PATH}/features.csv", index=False)


if __name__ == "__main__":
    main()
