import os
import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

ALERTS_FILE_PATH = "data/alerts.json"
SEED_FILE_PATH = "data/seed_alerts.json"

class AlertBase(BaseModel):
    title: str = Field(..., description="Title of the alert")
    description: str = Field(..., description="Detailed description of the alert")
    severity: str = Field("info", description="Severity level: info, warning, critical")
    status: str = Field("active", description="Status of the alert: active, resolved, acknowledged")
    latitude: Optional[float] = Field(None, description="Latitude for spatial alerts")
    longitude: Optional[float] = Field(None, description="Longitude for spatial alerts")
    affected_roads_count: Optional[int] = Field(None, description="Number of roads affected within the buffer area")
    affected_buildings_count: Optional[int] = Field(None, description="Number of buildings affected within the buffer area")
    affected_amenities_count: Optional[int] = Field(None, description="Number of amenities affected within the buffer area")
    affected_population: Optional[float] = Field(None, description="Population affected within the buffer area")

class AlertCreate(AlertBase):
    id: Optional[str] = Field(None, description="Optional custom ID of the alert")
    created_at: Optional[str] = Field(None, description="Optional custom ISO creation timestamp")
    updated_at: Optional[str] = Field(None, description="Optional custom ISO update timestamp")

class AlertUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    affected_roads_count: Optional[int] = None
    affected_buildings_count: Optional[int] = None
    affected_amenities_count: Optional[int] = None
    affected_population: Optional[float] = None

class TraceEntry(BaseModel):
    timestamp: str = Field(..., description="Timestamp of the change")
    change_type: str = Field(..., description="Type of change: create, update")
    changes: List[dict] = Field(default=[], description="List of individual field changes: [{'field': 'status', 'old_value': 'active', 'new_value': 'resolved'}]")
    info: Optional[str] = Field(None, description="Additional context or summary")

class Alert(AlertBase):
    id: str = Field(..., description="Unique identifier of the alert")
    created_at: str = Field(..., description="ISO 8601 formatted creation timestamp")
    updated_at: str = Field(..., description="ISO 8601 formatted update timestamp")
    trace: List[TraceEntry] = Field(default=[], description="Auditable trace logs for the alert")


# Cache for roads GeoDataFrame to avoid reloading on every request
ROADS_GDF = None
BUILDINGS_GDF = None
AMENITIES_GDF = None

def get_roads_gdf():
    global ROADS_GDF
    if ROADS_GDF is None:
        try:
            import geopandas as gpd
            roads_path = "data/exposure/roads_with_risk.geojson"
            if os.path.exists(roads_path):
                ROADS_GDF = gpd.read_file(roads_path)
            else:
                ROADS_GDF = gpd.GeoDataFrame()
        except Exception as e:
            print(f"Error loading roads_with_risk.geojson: {e}")
            import geopandas as gpd
            ROADS_GDF = gpd.GeoDataFrame()
    return ROADS_GDF

def get_buildings_gdf():
    global BUILDINGS_GDF
    if BUILDINGS_GDF is None:
        try:
            import geopandas as gpd
            path = "data/exposure/buildings_with_risk.geojson"
            if os.path.exists(path):
                BUILDINGS_GDF = gpd.read_file(path)
            else:
                BUILDINGS_GDF = gpd.GeoDataFrame()
        except Exception as e:
            print(f"Error loading buildings_with_risk.geojson: {e}")
            import geopandas as gpd
            BUILDINGS_GDF = gpd.GeoDataFrame()
    return BUILDINGS_GDF

def get_amenities_gdf():
    global AMENITIES_GDF
    if AMENITIES_GDF is None:
        try:
            import geopandas as gpd
            path = "data/exposure/amenities_with_risk.geojson"
            if os.path.exists(path):
                AMENITIES_GDF = gpd.read_file(path)
            else:
                AMENITIES_GDF = gpd.GeoDataFrame()
        except Exception as e:
            print(f"Error loading amenities_with_risk.geojson: {e}")
            import geopandas as gpd
            AMENITIES_GDF = gpd.GeoDataFrame()
    return AMENITIES_GDF

def calculate_affected_roads(latitude: Optional[float], longitude: Optional[float], buffer_radius: float = 0.01) -> Optional[int]:
    if latitude is None or longitude is None:
        return None
    try:
        from shapely.geometry import Point
        gdf = get_roads_gdf()
        if gdf is None or gdf.empty:
            return 0
        point = Point(longitude, latitude)
        buffered_point = point.buffer(buffer_radius)
        # Find intersecting roads
        intersecting = gdf[gdf.geometry.intersects(buffered_point)]
        return int(len(intersecting))
    except Exception as e:
        print(f"Error calculating affected roads: {e}")
        return 0

def calculate_affected_buildings(latitude: Optional[float], longitude: Optional[float], buffer_radius: float = 0.01) -> Optional[int]:
    if latitude is None or longitude is None:
        return None
    try:
        from shapely.geometry import Point
        gdf = get_buildings_gdf()
        if gdf is None or gdf.empty:
            return 0
        point = Point(longitude, latitude)
        buffered_point = point.buffer(buffer_radius)
        intersecting = gdf[gdf.geometry.intersects(buffered_point)]
        return int(len(intersecting))
    except Exception as e:
        print(f"Error calculating affected buildings: {e}")
        return 0

def calculate_affected_amenities(latitude: Optional[float], longitude: Optional[float], buffer_radius: float = 0.01) -> Optional[int]:
    if latitude is None or longitude is None:
        return None
    try:
        from shapely.geometry import Point
        gdf = get_amenities_gdf()
        if gdf is None or gdf.empty:
            return 0
        point = Point(longitude, latitude)
        buffered_point = point.buffer(buffer_radius)
        intersecting = gdf[gdf.geometry.intersects(buffered_point)]
        return int(len(intersecting))
    except Exception as e:
        print(f"Error calculating affected amenities: {e}")
        return 0

def calculate_affected_population(latitude: Optional[float], longitude: Optional[float], buffer_radius: float = 0.01) -> Optional[float]:
    if latitude is None or longitude is None:
        return None
    try:
        import rasterio
        from rasterio.mask import mask
        from shapely.geometry import Point
        import numpy as np
        
        pop_path = "data/exposure/population.tif"
        if not os.path.exists(pop_path):
            return 0.0
            
        point = Point(longitude, latitude)
        buffered_point = point.buffer(buffer_radius)
        
        with rasterio.open(pop_path) as src:
            out_image, out_transform = mask(src, [buffered_point], crop=True)
            nodata = src.nodata
            if nodata is not None:
                valid_data = out_image[out_image != nodata]
            else:
                valid_data = out_image
            valid_data = valid_data[~np.isnan(valid_data)]
            return round(float(np.nansum(valid_data)), 2)
    except Exception as e:
        print(f"Error calculating affected population: {e}")
        return 0.0


def load_alerts() -> List[dict]:
    raw_alerts = []
    if not os.path.exists(ALERTS_FILE_PATH):
        os.makedirs(os.path.dirname(ALERTS_FILE_PATH), exist_ok=True)
        seed_data = []
        # if os.path.exists(SEED_FILE_PATH):
        #     try:
        #         with open(SEED_FILE_PATH, "r") as f:
        #             seed_data = json.load(f)
        #     except (json.JSONDecodeError, IOError):
        #         seed_data = []
        with open(ALERTS_FILE_PATH, "w") as f:
            json.dump(seed_data, f, indent=2)
        raw_alerts = seed_data
    else:
        try:
            with open(ALERTS_FILE_PATH, "r") as f:
                raw_alerts = json.load(f)
        except json.JSONDecodeError:
            raw_alerts = []

    # Backfill missing traces on loaded alerts for robust schema migration
    updated_any = False
    for alert in raw_alerts:
        if "trace" not in alert or not isinstance(alert["trace"], list):
            alert["trace"] = [
                {
                    "timestamp": alert.get("created_at", datetime.now(timezone.utc).isoformat()),
                    "change_type": "create",
                    "changes": [],
                    "info": "Alert registered (auto-backfilled log)"
                }
            ]
            updated_any = True
    
    if updated_any:
        save_alerts(raw_alerts)

    return raw_alerts

def save_alerts(alerts: List[dict]):
    os.makedirs(os.path.dirname(ALERTS_FILE_PATH), exist_ok=True)
    with open(ALERTS_FILE_PATH, "w") as f:
        json.dump(alerts, f, indent=2)


@router.get("/", response_model=List[Alert])
def get_alerts(severity: Optional[str] = None, status: Optional[str] = None):
    alerts = load_alerts()
    if severity:
        alerts = [a for a in alerts if a.get("severity") == severity]
    if status:
        alerts = [a for a in alerts if a.get("status") == status]
    # Sort by created_at descending (most recent first)
    alerts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return alerts


@router.get("/{alert_id}", response_model=Alert)
def get_alert(alert_id: str):
    alerts = load_alerts()
    for alert in alerts:
        if alert.get("id") == alert_id:
            return alert
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Alert with ID {alert_id} not found"
    )


@router.post("/", response_model=Alert, status_code=status.HTTP_201_CREATED)
def create_alert(alert_in: AlertCreate):
    alerts = load_alerts()
    now = datetime.now(timezone.utc).isoformat()
    created_at = alert_in.created_at if alert_in.created_at else now
    updated_at = alert_in.updated_at if alert_in.updated_at else now
    
    initial_trace = TraceEntry(
        timestamp=created_at,
        change_type="create",
        changes=[],
        info="Alert created via API / Dashboard UI"
    )
    
    affected_roads = calculate_affected_roads(alert_in.latitude, alert_in.longitude)
    affected_buildings = calculate_affected_buildings(alert_in.latitude, alert_in.longitude)
    affected_amenities = calculate_affected_amenities(alert_in.latitude, alert_in.longitude)
    affected_population = calculate_affected_population(alert_in.latitude, alert_in.longitude)
    
    new_alert = Alert(
        id=alert_in.id if alert_in.id else str(uuid.uuid4()),
        title=alert_in.title,
        description=alert_in.description,
        severity=alert_in.severity,
        status=alert_in.status,
        latitude=alert_in.latitude,
        longitude=alert_in.longitude,
        affected_roads_count=affected_roads,
        affected_buildings_count=affected_buildings,
        affected_amenities_count=affected_amenities,
        affected_population=affected_population,
        created_at=created_at,
        updated_at=updated_at,
        trace=[initial_trace]
    )
    
    alerts.append(new_alert.model_dump() if hasattr(new_alert, "model_dump") else new_alert.dict())
    save_alerts(alerts)
    return new_alert


@router.put("/{alert_id}", response_model=Alert)
def update_alert(alert_id: str, alert_in: AlertUpdate):
    if alert_in.status == "resolved":
        from routers.actions import load_actions
        actions = load_actions()
        open_actions = [
            a for a in actions
            if a.get("alert_id") == alert_id and a.get("status") not in ("completed", "cancelled")
        ]
        if open_actions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot resolve alert: there are pending or open actions. All actions must be completed or cancelled before resolving."
            )

    alerts = load_alerts()
    alert_idx = -1
    for idx, alert in enumerate(alerts):
        if alert.get("id") == alert_id:
            alert_idx = idx
            break
            
    if alert_idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID {alert_id} not found"
        )
        
    current_alert_dict = alerts[alert_idx]
    now = datetime.now(timezone.utc).isoformat()
    
    # Trace individual modifications
    changes = []
    update_data = alert_in.model_dump(exclude_unset=True) if hasattr(alert_in, "model_dump") else alert_in.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        old_val = current_alert_dict.get(key)
        if old_val != value:
            changes.append({
                "field": key,
                "old_value": old_val,
                "new_value": value
            })
            current_alert_dict[key] = value
            
    # If coordinates changed, recalculate affected metrics
    if any(c["field"] in ("latitude", "longitude") for c in changes):
        new_lat = current_alert_dict.get("latitude")
        new_lon = current_alert_dict.get("longitude")
        
        # Roads
        new_roads = calculate_affected_roads(new_lat, new_lon)
        if current_alert_dict.get("affected_roads_count") != new_roads:
            changes.append({
                "field": "affected_roads_count",
                "old_value": current_alert_dict.get("affected_roads_count"),
                "new_value": new_roads
            })
            current_alert_dict["affected_roads_count"] = new_roads
            
        # Buildings
        new_buildings = calculate_affected_buildings(new_lat, new_lon)
        if current_alert_dict.get("affected_buildings_count") != new_buildings:
            changes.append({
                "field": "affected_buildings_count",
                "old_value": current_alert_dict.get("affected_buildings_count"),
                "new_value": new_buildings
            })
            current_alert_dict["affected_buildings_count"] = new_buildings
            
        # Amenities
        new_amenities = calculate_affected_amenities(new_lat, new_lon)
        if current_alert_dict.get("affected_amenities_count") != new_amenities:
            changes.append({
                "field": "affected_amenities_count",
                "old_value": current_alert_dict.get("affected_amenities_count"),
                "new_value": new_amenities
            })
            current_alert_dict["affected_amenities_count"] = new_amenities
            
        # Population
        new_pop = calculate_affected_population(new_lat, new_lon)
        if current_alert_dict.get("affected_population") != new_pop:
            changes.append({
                "field": "affected_population",
                "old_value": current_alert_dict.get("affected_population"),
                "new_value": new_pop
            })
            current_alert_dict["affected_population"] = new_pop
            
    # If actual changes occurred, append a new trace log entry
    if changes:
        info_msg = f"Modified fields: {', '.join([c['field'] for c in changes])}"
        
        # Check if the alert is being resolved
        was_resolved = any(c["field"] == "status" and c["new_value"] == "resolved" for c in changes)
        if was_resolved:
            try:
                from routers.actions import load_actions
                all_actions = load_actions()
                attached_actions = [
                    a for a in all_actions if a.get("alert_id") == alert_id
                ]
                if attached_actions:
                    actions_str = ", ".join([f"'{a.get('title')}' ({a.get('status')})" for a in attached_actions])
                    info_msg = f"Alert marked as RESOLVED. Attached response actions: {actions_str}"
                else:
                    info_msg = "Alert marked as RESOLVED. No response actions were attached."
            except Exception as e:
                info_msg = f"Alert marked as RESOLVED. (Failed to load actions: {e})"

        trace_entry = {
            "timestamp": now,
            "change_type": "update",
            "changes": changes,
            "info": info_msg
        }
        if "trace" not in current_alert_dict or not isinstance(current_alert_dict["trace"], list):
            current_alert_dict["trace"] = []
        current_alert_dict["trace"].append(trace_entry)
        current_alert_dict["updated_at"] = now
    
    alerts[alert_idx] = current_alert_dict
    save_alerts(alerts)
    return current_alert_dict


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: str):
    alerts = load_alerts()
    alert_idx = -1
    for idx, alert in enumerate(alerts):
        if alert.get("id") == alert_id:
            alert_idx = idx
            break
            
    if alert_idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID {alert_id} not found"
        )
        
    alerts.pop(alert_idx)
    save_alerts(alerts)
    return
