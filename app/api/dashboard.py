from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.dashboard import WebsiteDashboardItem
from app.models.website import Website
from app.models.check_result import CheckResult
from app.models.website_metrics import WebsiteMetrics
from app.models.alert_event import AlertEvent

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("s", response_model=list[WebsiteDashboardItem])
def get_dashboard_websites(db: Session = Depends(get_db)):
    websites = db.query(Website).filter(Website.is_active == True).all()
    response = []

    for site in websites:
        latest_check = (
            db.query(CheckResult)
            .filter(CheckResult.website_id == site.id)
            .order_by(CheckResult.checked_at.desc())
            .first()
        )

        metrics = (
            db.query(WebsiteMetrics)
            .filter(WebsiteMetrics.website_id == site.id)
            .first()
        )

        # Current status logic
        is_up = latest_check.is_up if latest_check else False
        current_status = "up" if is_up else "down"

        # Alert logic
        alert_state = "normal"

        if metrics.consecutive_failures >= 5:
            alert_state = "critical"
        elif metrics.avg_response_time_ms and metrics.avg_response_time_ms > 2000:
            alert_state = "warning"

        response.append(
            WebsiteDashboardItem(
                id=site.id,
                name=site.name,
                url=site.url,

                current_status=current_status,
                is_up=is_up,

                uptime_percentage=metrics.uptime_percentage if metrics else 0.0,
                avg_response_time_ms=metrics.avg_response_time if metrics else None,

                last_checked_at=latest_check.checked_at if latest_check else None,
                alert_state=alert_state,
            )
        )

    return response

@router.get("/alerts")
def get_active_alerts(db: Session = Depends(get_db)):
    return db.query(AlertEvent).filter(AlertEvent.is_active == True).order_by(AlertEvent.triggered_at.desc()).all()
