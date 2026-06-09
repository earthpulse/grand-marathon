import os
import json
import math
import pandas as pd
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from matplotlib import cm
from matplotlib.colors import ListedColormap

from spai.storage.LocalStorage import LocalStorage
from spai.image.xyz import get_image_data, get_tile_data, ready_image
from spai.image.xyz.errors import ImageOutOfBounds

# Define a custom colormap for risk mapping:

risk_colors = [
    [0.0, 0.0, 0.0, 0.0],  # 0: transparent
    # [0.13, 0.55, 0.13, 1.0],   # 1: green (Forest Green)
    [0.0, 0.0, 0.0, 0.0],  # 1: green (Forest Green)
    # [1.0, 0.84, 0.0, 1.0],     # 2: yellow (Gold)
    [0.0, 0.0, 0.0, 0.0],  # 2: yellow (Gold)
    # [1.0, 0.5, 0.0, 1.0],      # 3: orange
    [0.0, 0.0, 0.0, 0.0],  # 3: orange
    [0.86, 0.08, 0.24, 1.0],  # 4: red (Crimson)
]
risk_cmap = ListedColormap(risk_colors)
setattr(cm, "risk_palette", risk_cmap)
setattr(cm, "risk_palette_4", risk_cmap)
risk_colors_3 = [
    [0.0, 0.0, 0.0, 0.0],  # 0: transparent
    [0.0, 0.0, 0.0, 0.0],  # 1: green (Forest Green)
    # [1.0, 0.84, 0.0, 1.0],     # 2: yellow (Gold)
    [0.0, 0.0, 0.0, 0.0],  # 2: yellow (Gold)
    [0.86, 0.08, 0.24, 1.0],  # 3: red
]
risk_cmap_3 = ListedColormap(risk_colors_3)
setattr(cm, "risk_palette_3", risk_cmap_3)

router = APIRouter()

storage = LocalStorage("data")


def parse_stretch(stretch: str) -> tuple[float, float]:
    values = tuple(float(value) for value in stretch.split(","))
    if len(values) != 2:
        raise ValueError("stretch must contain exactly two comma-separated values")
    return values


def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(x) for x in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj


@router.get("/aoi")
def retrieve_aoi():
    aoi_gdf = storage.read("aois/seadur.geojson")
    geojson = aoi_gdf.__geo_interface__
    return JSONResponse(content=geojson)


@router.get("/dates")
def retrieve_dates():
    hotspots = storage.read("hotspots_filtered.geojson")
    hotspots_dates = sorted(hotspots.ACQ_DATE.unique())
    hotspots_dates = [
        pd.Timestamp(date).strftime("%Y-%m-%d") for date in hotspots_dates
    ]

    dates_list = [f"2025-08-{str(day).zfill(2)}" for day in range(1, 23)]

    # Calculate colors for each date
    date_colors = {}
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    for date in dates_list:
        file_path = os.path.join(
            base_dir, "data", "final_risk_analytics", f"analytics_{date}.json"
        )
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                mean_hazard = data.get("mean_hazard", 0.0)
                if mean_hazard < 0.25:
                    date_colors[date] = "green"
                elif mean_hazard < 0.45:
                    date_colors[date] = "yellow"
                else:
                    date_colors[date] = "red"
            except Exception:
                date_colors[date] = "green"
        else:
            date_colors[date] = "green"

    return {
        "hotspot_dates": hotspots_dates,
        "dates": dates_list,
        "today": "2026-08-15",
        "date_colors": date_colors,
    }


@router.get("/analytics/{date}")
def retrieve_analytics(date: str):
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    file_path = os.path.join(
        base_dir, "data", "final_risk_analytics", f"analytics_with_risk_{date}.json"
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analytics not found for date {date}",
        )

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading analytics: {str(e)}",
        )


@router.get("/hotspots")
def retrieve_hotspots():
    hotspots = storage.read("hotspots_buffered.geojson")
    # Convert all non-serializable objects (like Timestamp) to strings in properties
    geojson = hotspots.__geo_interface__
    for feature in geojson.get("features", []):
        props = feature.get("properties", {})
        for k, v in props.items():
            if isinstance(v, pd.Timestamp):
                props[k] = v.strftime("%Y-%m-%d")
    return JSONResponse(content=geojson)


@router.get("/exposure/amenities")
def retrieve_exposure_amenities():
    try:
        gdf_risk = storage.read("exposure/amenities_with_risk.geojson")
        # try:
        #     gdf_orig = storage.read("exposure/amenities.geojson")
        #     gdf_orig_df = pd.DataFrame(gdf_orig.drop(columns="geometry"))
        #     gdf_risk["id"] = gdf_risk["id"].astype(str)
        #     gdf_orig_df["id"] = gdf_orig_df["id"].astype(str)
        #     merged = gdf_risk.merge(gdf_orig_df, on="id", how="left")
        # except Exception as e:
        #     print("Failed to merge amenities:", e)
        #     merged = gdf_risk
        # geojson = clean_nan(merged.__geo_interface__)
        geojson = clean_nan(gdf_risk.__geo_interface__)
        return JSONResponse(content=geojson)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/exposure/buildings")
def retrieve_exposure_buildings():
    try:
        gdf = storage.read("exposure/buildings_with_risk.geojson")
        geojson = clean_nan(gdf.__geo_interface__)
        return JSONResponse(content=geojson)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/exposure/roads")
def retrieve_exposure_roads():
    try:
        gdf = storage.read("exposure/roads_with_risk.geojson")
        geojson = clean_nan(gdf.__geo_interface__)
        return JSONResponse(content=geojson)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/vulnerability/municipalities")
def retrieve_vulnerability_municipalities():
    try:
        gdf = storage.read("vulnerability/municipalities_vulnerability.geojson")
        geojson = gdf.__geo_interface__
        return JSONResponse(content=geojson)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/xyz/{image:path}/{z}/{x}/{y}.png")
def retrieve_image_tile(
    image: str,
    z: int,
    x: int,
    y: int,
    bands: str = "1",
    stretch: str = "0,1",
    palette: str = "RdYlGn_r",
):
    image_path = storage.get_path(image + ".tif")
    tile_size = (256, 256)
    if len(bands) == 1:
        bands = int(bands)
    else:
        bands = tuple([int(band) for band in bands.split(",")])
    stretch = parse_stretch(stretch)
    try:
        tile = get_tile_data(image_path, (x, y, z), bands, tile_size)
        tile = get_image_data(tile, stretch, palette)
        image = ready_image(tile)
        return StreamingResponse(image, media_type="image/png")
    except ImageOutOfBounds as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
