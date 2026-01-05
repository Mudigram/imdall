from sqlalchemy.orm import Session
from app.models.check_result import CheckResult
from app.models.website_metrics import WebsiteMetrics
from app.models.alert_event import AlertEvent

def check_consecutive_failures(
    db: Session,
    website_id: int,
    threshold: int = 3
):
    recent_checks = (
        db.query(CheckResult)
        .filter(CheckResult.website_id == website_id)
        .order_by(CheckResult.checked_at.desc())
        .limit(threshold)
        .all()
    )

    if len(recent_checks) < threshold:
        return

    if all(not c.is_up for c in recent_checks):
        create_alert(
            db,
            website_id,
            "consecutive_failures",
            f"Website down {threshold} times consecutively"
        )


def check_uptime_threshold(
    db: Session,
    website_id: int,
    min_uptime: float = 90.0
):
    metric = (
        db.query(WebsiteMetrics)
        .filter(WebsiteMetrics.website_id == website_id)
        .order_by(WebsiteMetrics.calculated_at.desc())
        .first()
    )

    if metric and metric.uptime_percentage < min_uptime:
        create_alert(
            db,
            website_id,
            "low_uptime",
            f"Uptime below {min_uptime}% in last 24h"
        )


def create_alert(
    db: Session,
    website_id: int,
    alert_type: str,
    message: str
):
    existing = (
        db.query(AlertEvent)
        .filter(
            AlertEvent.website_id == website_id,
            AlertEvent.alert_type == alert_type,
            AlertEvent.is_active == True
        )
        .first()
    )

    if existing:
        return

    alert = AlertEvent(
        website_id=website_id,
        alert_type=alert_type,
        message=message
    )

    db.add(alert)
    db.commit()
