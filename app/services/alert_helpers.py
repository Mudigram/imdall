from sqlalchemy.orm import Session
from app.models.alert_event import AlertEvent


def trigger_alert_if_needed(
    db: Session,
    website_id: int,
    alert_type: str,
    message: str
) -> bool:
    """
    Trigger an alert if it doesn't already exist.
    Returns True if a new alert was created, False otherwise.
    """
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
        return False

    alert = AlertEvent(
        website_id=website_id,
        alert_type=alert_type,
        message=message
    )
    db.add(alert)
    return True


def resolve_alert_if_needed(
    db: Session,
    website_id: int,
    alert_type: str
) -> bool:
    """
    Resolve an active alert if it exists.
    Returns True if an alert was resolved, False otherwise.
    """
    active_alert = (
        db.query(AlertEvent)
        .filter(
            AlertEvent.website_id == website_id,
            AlertEvent.alert_type == alert_type,
            AlertEvent.is_active == True
        )
        .first()
    )

    if not active_alert:
        return False

    active_alert.is_active = False
    return True
