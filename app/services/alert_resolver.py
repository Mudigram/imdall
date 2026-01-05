from app.models.alert import Alert
from datetime import datetime

def resolve_alert_if_needed(db, website_id: int, alert_type: str):
    active_alert = (
        db.query(Alert)
        .filter(
            Alert.website_id == website_id,
            Alert.alert_type == alert_type,
            Alert.resolved_at.is_(None)
        )
        .first()
    )

    if active_alert:
        active_alert.resolved_at = datetime.utcnow()
        db.commit()
