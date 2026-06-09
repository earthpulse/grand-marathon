import geopandas as gpd
from datetime import date
import xarray as xr
import os
import numpy as np

from spai.data.climate.reanalysis_land_era5 import ERA5_VARS, check_access, aoi_to_0360_parts, _to180, _to0360
from spai.data.climate.area_of_interest import AreaOfInterest

PAT = os.getenv(
    "EARTH_DATA_HUB_PAT"
)  #  https://earthdatahub.destine.eu/account-settings

def load_era5(
    aoi: gpd.GeoDataFrame,
    start_date: date,
    end_date: date | None = None,
    dataset: str = "reanalysis-era5-land-no-antartica-v0",
    era5_vars: list[str, None] = [],
) -> xr.Dataset:

    # print("holaaaa", PAT)
    
    aoi = AreaOfInterest.from_geodataframe(aoi)

    if end_date is None:
        end_date = start_date

    if start_date > end_date:
        raise ValueError("Start date must be before or equal to end_date")

    if era5_vars and not set(era5_vars).issubset(ERA5_VARS):
        raise ValueError(
            f"At least one of the passed vars is not in allowed vars: {ERA5_VARS}"
        )

    #url = f"https://edh:{PAT}@data.earthdatahub.destine.eu/era5/{dataset}.zarr"
    url = f"https://edh:{PAT}@api.earthdatahub.destine.eu/era5/{dataset}.zarr"

    check_access(url)

    if not PAT:
        raise ValueError(
            "No PAT found for Earth Data Hub, please set EARTH_DATA_HUB_PAT on https://earthdatahub.destine.eu/ and store in your .env"
        )

    parts = aoi_to_0360_parts(aoi)
    datasets = []

    for p in parts:
        ds = xr.open_dataset(
            url,
            storage_options={"client_kwargs": {"trust_env": True}},
            chunks={},
            engine="zarr",
        )

        data = ds.sel(
            valid_time=slice(
                np.datetime64(start_date),
                np.datetime64(end_date) + np.timedelta64(1, "D"),
            ),
            latitude=slice(p["ymax"], p["ymin"]),
            longitude=slice(p["xmin"], p["xmax"]),
        )

        if era5_vars:
            data = data[era5_vars]

        if data.valid_time.size == 0:
            raise ValueError(
                "No data available to download for the specified date range"
            )
        datasets.append(data)

    ds = xr.concat(datasets, dim="longitude") if len(datasets) > 1 else datasets[0]
    ds = ds.assign_coords(longitude=_to180(ds.longitude)).sortby("longitude")

    return ds
