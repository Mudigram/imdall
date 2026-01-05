from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.alert_event import AlertEvent
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
def list_alerts(
    active: bool | None = True,
    db: Session = Depends(get_db)
):
    query = db.query(AlertEvent)
    if active is not None:
        query = query.filter(AlertEvent.is_active == active)
    return query.order_by(AlertEvent.triggered_at.desc()).all()

@router.get("/history")
def get_alert_history(db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .order_by(Alert.triggered_at.desc())
        .limit(100)
        .all()
    )
