import io
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from starlette.responses import StreamingResponse
from weasyprint import HTML
from jinja2 import Template
from .alerts import load_alerts
from .actions import load_actions

router = APIRouter()


def parse_iso_datetime(iso_str: str) -> datetime:
    if iso_str.endswith("Z"):
        iso_str = iso_str[:-1] + "+00:00"
    return datetime.fromisoformat(iso_str)


@router.get("/download")
def download_report_pdf():
    try:
        # Load Alerts & Actions
        raw_alerts = load_alerts()
        raw_actions = load_actions()

        # Calculate summary metrics (KPIs)
        total_alerts = len(raw_alerts)
        active_alerts = len([a for a in raw_alerts if a.get("status") == "active"])
        resolved_alerts = len([a for a in raw_alerts if a.get("status") == "resolved"])
        total_actions = len(raw_actions)

        events = []

        # 1. Parse Alert Registrations (Creation)
        for alert in raw_alerts:
            created_at_str = alert.get("created_at", "")
            if created_at_str:
                date_str = created_at_str[:10]
                dt = parse_iso_datetime(created_at_str)
                events.append(
                    {
                        "id": f"alert-create-{alert.get('id')}",
                        "date": date_str,
                        "timestamp": dt,
                        "time_str": dt.strftime("%I:%M %p"),
                        "type": "alert_create",
                        "category": "hazard",
                        "title": "🚨 New Alert Registered",
                        "subtitle": alert.get("title", ""),
                        "severity": alert.get("severity", "info"),
                        "icon": "🚨",
                        "description": alert.get("description", ""),
                        "latitude": alert.get("latitude"),
                        "longitude": alert.get("longitude"),
                        "changes": [],
                    }
                )

            # 2. Parse Alert Audit Traces
            for index, tr in enumerate(alert.get("trace", [])):
                if tr.get("change_type") == "update":
                    timestamp_str = tr.get("timestamp", "")
                    if timestamp_str:
                        date_str = timestamp_str[:10]
                        dt = parse_iso_datetime(timestamp_str)
                        events.append(
                            {
                                "id": f"alert-trace-{alert.get('id')}-{index}",
                                "date": date_str,
                                "timestamp": dt,
                                "time_str": dt.strftime("%I:%M %p"),
                                "type": "alert_update",
                                "category": "lifecycle",
                                "title": "🔄 Alert Status Updated",
                                "subtitle": alert.get("title", ""),
                                "severity": alert.get("severity", "info"),
                                "icon": "🔄",
                                "description": tr.get("info")
                                or "Status configuration updated.",
                                "changes": tr.get("changes") or [],
                            }
                        )

        # 3. Parse Response Actions Deployed
        for action in raw_actions:
            created_at_str = action.get("created_at", "")
            if created_at_str:
                date_str = created_at_str[:10]
                dt = parse_iso_datetime(created_at_str)
                events.append(
                    {
                        "id": f"action-create-{action.get('id')}",
                        "date": date_str,
                        "timestamp": dt,
                        "time_str": dt.strftime("%I:%M %p"),
                        "type": "action_deploy",
                        "category": "response",
                        "title": "🚀 Response Action Deployed",
                        "subtitle": action.get("title", ""),
                        "severity": "info",
                        "icon": "🚒",
                        "description": action.get("description", ""),
                        "changes": [],
                        "meta": {"status": action.get("status", "pending")},
                    }
                )

            # 4. Parse Action Traces
            for index, tr in enumerate(action.get("trace", [])):
                if tr.get("change_type") == "update":
                    timestamp_str = tr.get("timestamp", "")
                    if timestamp_str:
                        date_str = timestamp_str[:10]
                        dt = parse_iso_datetime(timestamp_str)
                        events.append(
                            {
                                "id": f"action-trace-{action.get('id')}-{index}",
                                "date": date_str,
                                "timestamp": dt,
                                "time_str": dt.strftime("%I:%M %p"),
                                "type": "action_update",
                                "category": "response",
                                "title": "⚙️ Response Progress Updated",
                                "subtitle": action.get("title", ""),
                                "severity": "info",
                                "icon": "📋",
                                "description": tr.get("info")
                                or f"Task status advanced to {action.get('status', 'pending')}.",
                                "changes": tr.get("changes") or [],
                                "meta": {"status": action.get("status", "pending")},
                            }
                        )

        # Group by Day
        groups_dict = {}
        for event in events:
            day = event["date"]
            if day not in groups_dict:
                groups_dict[day] = []
            groups_dict[day].append(event)

        sorted_days = sorted(groups_dict.keys())

        groups = []
        for day in sorted_days:
            # Sort events in the day chronologically
            day_events = sorted(groups_dict[day], key=lambda e: e["timestamp"])

            # Format the day date string nicely
            dt_day = datetime.strptime(day, "%Y-%m-%d")
            formatted_date = dt_day.strftime("%A, %B %d, %Y")

            groups.append(
                {
                    "day": day,
                    "formatted_date": formatted_date,
                    "events": day_events,
                }
            )

        # Load and render Jinja2 Template
        with open("api/templates/report_template.html", "r") as f:
            template_content = f.read()

        template = Template(template_content)
        rendered_html = template.render(
            total_alerts=total_alerts,
            active_alerts=active_alerts,
            resolved_alerts=resolved_alerts,
            total_actions=total_actions,
            groups=groups,
        )

        # Compile HTML to PDF using WeasyPrint
        pdf_bytes = HTML(string=rendered_html).write_pdf()

        # Return PDF streaming response
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=incident_report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
            },
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compile PDF report: {str(e)}",
        )
