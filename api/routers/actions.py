import os
import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

ACTIONS_FILE_PATH = "data/actions.json"
SEED_ACTIONS_FILE_PATH = "data/seed_actions.json"

class ActionBase(BaseModel):
    alert_id: str = Field(..., description="ID of the alert this action is linked to")
    title: str = Field(..., description="Title of the action")
    description: str = Field(..., description="Detailed description of the action")
    status: str = Field("pending", description="Status of the action: pending, in_progress, completed, cancelled")
    predefined_id: Optional[str] = Field(None, description="Optional ID of the predefined template this action was created from")

class ActionCreate(ActionBase):
    id: Optional[str] = Field(None, description="Optional custom ID of the action")
    created_at: Optional[str] = Field(None, description="Optional custom ISO creation timestamp")
    updated_at: Optional[str] = Field(None, description="Optional custom ISO update timestamp")

class ActionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    alert_id: Optional[str] = None
    predefined_id: Optional[str] = None

class TraceEntry(BaseModel):
    timestamp: str = Field(..., description="Timestamp of the change")
    change_type: str = Field(..., description="Type of change: create, update")
    changes: List[dict] = Field(default=[], description="List of individual field changes: [{'field': 'status', 'old_value': 'pending', 'new_value': 'in_progress'}]")
    info: Optional[str] = Field(None, description="Additional context or summary")

class Action(ActionBase):
    id: str = Field(..., description="Unique identifier of the action")
    created_at: str = Field(..., description="ISO 8601 formatted creation timestamp")
    updated_at: str = Field(..., description="ISO 8601 formatted update timestamp")
    trace: List[TraceEntry] = Field(default=[], description="Auditable trace logs for the action")


# Predefined Actions List
PREDEFINED_ACTIONS = [
    {
        "id": "deploy_crew",
        "title": "Deploy Ground Firefighting Crew",
        "description": "Coordinate with local emergency services to deploy ground crew to the affected coordinates for containment and extinguishing."
    },
    {
        "id": "evacuate_area",
        "title": "Issue Precautionary Evacuation Order",
        "description": "Coordinate with civil protection to establish evacuation routes and notify residents within the critical zone."
    },
    {
        "id": "aerial_recon",
        "title": "Request Aerial Support & Water Bomber Dispatch",
        "description": "Dispatch helicopter or water bomber aircraft to scout the fire's progression and perform targeted drops."
    },
    {
        "id": "establish_firebreak",
        "title": "Construct Mechanical Firebreak Line",
        "description": "Deploy bulldozers and heavy machinery to clear combustible vegetation and create an active barrier along the fire's path."
    },
    {
        "id": "public_smoke_alert",
        "title": "Issue Public Smoke & Health Advisory",
        "description": "Publish regional air quality warnings, advising nearby communities to close windows and remain indoors."
    },
    {
        "id": "inspect_roads",
        "title": "Inspect Affected Roads",
        "description": "Dispatch emergency crews to inspect transport routes, clear debris, and set up road blocks if necessary to ensure safe transit."
    },
    {
        "id": "check_buildings",
        "title": "Conduct Building Safety Checks",
        "description": "Conduct search and rescue or precautionary safety sweeps of residential and commercial structures within the buffer zone."
    },
    {
        "id": "secure_amenities",
        "title": "Secure Critical Infrastructure",
        "description": "Deploy security and engineering teams to protect local amenities, schools, healthcare clinics, and utilities from threat."
    }
]


def load_actions() -> List[dict]:
    raw_actions = []
    if not os.path.exists(ACTIONS_FILE_PATH):
        os.makedirs(os.path.dirname(ACTIONS_FILE_PATH), exist_ok=True)
        seed_data = []
        # if os.path.exists(SEED_ACTIONS_FILE_PATH):
        #     try:
        #         with open(SEED_ACTIONS_FILE_PATH, "r") as f:
        #             seed_data = json.load(f)
        #     except (json.JSONDecodeError, IOError):
        #         seed_data = []
        with open(ACTIONS_FILE_PATH, "w") as f:
            json.dump(seed_data, f, indent=2)
        raw_actions = seed_data
    else:
        try:
            with open(ACTIONS_FILE_PATH, "r") as f:
                raw_actions = json.load(f)
        except json.JSONDecodeError:
            raw_actions = []

    # Backfill missing traces on loaded actions for robust schema migration
    updated_any = False
    for action in raw_actions:
        if "trace" not in action or not isinstance(action["trace"], list):
            action["trace"] = [
                {
                    "timestamp": action.get("created_at", datetime.now(timezone.utc).isoformat()),
                    "change_type": "create",
                    "changes": [],
                    "info": "Action registered (auto-backfilled log)"
                }
            ]
            updated_any = True
    
    if updated_any:
        save_actions(raw_actions)

    return raw_actions

def save_actions(actions: List[dict]):
    os.makedirs(os.path.dirname(ACTIONS_FILE_PATH), exist_ok=True)
    with open(ACTIONS_FILE_PATH, "w") as f:
        json.dump(actions, f, indent=2)


@router.get("/predefined")
def get_predefined_actions():
    return PREDEFINED_ACTIONS


@router.get("/", response_model=List[Action])
def get_actions(alert_id: Optional[str] = None, status: Optional[str] = None):
    actions = load_actions()
    if alert_id:
        actions = [a for a in actions if a.get("alert_id") == alert_id]
    if status:
        actions = [a for a in actions if a.get("status") == status]
    # Sort by created_at descending (most recent first)
    actions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return actions


@router.get("/{action_id}", response_model=Action)
def get_action(action_id: str):
    actions = load_actions()
    for action in actions:
        if action.get("id") == action_id:
            return action
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Action with ID {action_id} not found"
    )


@router.post("/", response_model=Action, status_code=status.HTTP_201_CREATED)
def create_action(action_in: ActionCreate):
    actions = load_actions()
    now = datetime.now(timezone.utc).isoformat()
    created_at = action_in.created_at if action_in.created_at else now
    updated_at = action_in.updated_at if action_in.updated_at else now
    
    initial_trace = TraceEntry(
        timestamp=created_at,
        change_type="create",
        changes=[],
        info="Action created via API / Act Page UI"
    )
    
    new_action = Action(
        id=action_in.id if action_in.id else str(uuid.uuid4()),
        alert_id=action_in.alert_id,
        title=action_in.title,
        description=action_in.description,
        status=action_in.status,
        predefined_id=action_in.predefined_id,
        created_at=created_at,
        updated_at=updated_at,
        trace=[initial_trace]
    )
    
    actions.append(new_action.model_dump() if hasattr(new_action, "model_dump") else new_action.dict())
    save_actions(actions)

    # Update the linked alert's trace to log that a new action was attached
    try:
        from routers.alerts import load_alerts, save_alerts
        alerts = load_alerts()
        for alert in alerts:
            if alert.get("id") == action_in.alert_id:
                if "trace" not in alert or not isinstance(alert["trace"], list):
                    alert["trace"] = []
                alert["trace"].append({
                    "timestamp": created_at,
                    "change_type": "update",
                    "changes": [],
                    "info": f"Response action attached: '{action_in.title}' (Status: {action_in.status})"
                })
                alert["updated_at"] = created_at
                save_alerts(alerts)
                break
    except Exception as e:
        print(f"Failed to log action attachment to alert trace: {e}")

    return new_action


@router.put("/{action_id}", response_model=Action)
def update_action(action_id: str, action_in: ActionUpdate):
    actions = load_actions()
    action_idx = -1
    for idx, action in enumerate(actions):
        if action.get("id") == action_id:
            action_idx = idx
            break
            
    if action_idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )
        
    current_action_dict = actions[action_idx]
    now = datetime.now(timezone.utc).isoformat()
    
    # Trace individual modifications
    changes = []
    update_data = action_in.model_dump(exclude_unset=True) if hasattr(action_in, "model_dump") else action_in.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        old_val = current_action_dict.get(key)
        if old_val != value:
            changes.append({
                "field": key,
                "old_value": old_val,
                "new_value": value
            })
            current_action_dict[key] = value
            
    # If actual changes occurred, append a new trace log entry
    if changes:
        trace_entry = {
            "timestamp": now,
            "change_type": "update",
            "changes": changes,
            "info": f"Modified fields: {', '.join([c['field'] for c in changes])}"
        }
        if "trace" not in current_action_dict or not isinstance(current_action_dict["trace"], list):
            current_action_dict["trace"] = []
        current_action_dict["trace"].append(trace_entry)
        current_action_dict["updated_at"] = now
        
        # If status of the action changed, also log it in the linked alert's trace
        status_change = next((c for c in changes if c["field"] == "status"), None)
        if status_change:
            try:
                from routers.alerts import load_alerts, save_alerts
                alerts = load_alerts()
                for alert in alerts:
                    if alert.get("id") == current_action_dict.get("alert_id"):
                        if "trace" not in alert or not isinstance(alert["trace"], list):
                            alert["trace"] = []
                        alert["trace"].append({
                            "timestamp": now,
                            "change_type": "update",
                            "changes": [],
                            "info": f"Action '{current_action_dict.get('title')}' status updated: {status_change['old_value']} ➔ {status_change['new_value']}"
                        })
                        alert["updated_at"] = now
                        save_alerts(alerts)
                        break
            except Exception as e:
                print(f"Failed to log action status change to alert trace: {e}")
    
    actions[action_idx] = current_action_dict
    save_actions(actions)
    return current_action_dict


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action(action_id: str):
    actions = load_actions()
    action_idx = -1
    for idx, action in enumerate(actions):
        if action.get("id") == action_id:
            action_idx = idx
            break
            
    if action_idx == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )
        
    actions.pop(action_idx)
    save_actions(actions)
    return
