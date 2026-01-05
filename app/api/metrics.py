from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.website_metrics import WebsiteMetrics
from app.schemas.timeline import TimelinePoint
from app.models.check_result import CheckResult
from datetime import datetime, timedelta

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/{website_id}")
def get_metrics(
    website_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(WebsiteMetrics)
        .filter(WebsiteMetrics.website_id == website_id)
        .order_by(WebsiteMetrics.calculated_at.desc())
        .first()
    )

@router.get(
    "/websites/{website_id}/uptime",
    response_model=list[TimelinePoint]
)
def get_uptime_timeline(
    website_id: int,
    hours: int = 24,
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(hours=hours)

    checks = (
        db.query(CheckResult)
        .filter(
            CheckResult.website_id == website_id,
            CheckResult.checked_at >= since,
        )
        .order_by(CheckResult.checked_at.asc())
        .all()
    )

    return [
        TimelinePoint(
            timestamp=check.checked_at,
            value=1 if check.is_up else 0
        )
        for check in checks
    ]

@router.get(
    "/websites/{website_id}/response-times",
    response_model=list[TimelinePoint]
)
def get_response_time_timeline(
    website_id: int,
    hours: int = 24,
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(hours=hours)

    checks = (
        db.query(CheckResult)
        .filter(
            CheckResult.website_id == website_id,
            CheckResult.checked_at >= since,
            CheckResult.response_time.isnot(None),
        )
        .order_by(CheckResult.checked_at.asc())
        .all()
    )

    return [
        TimelinePoint(
            timestamp=check.checked_at,
            value=check.response_time
        )
        for check in checks
    ]

@router.get("/websites/{website_id}/checks")
def get_recent_checks(
    website_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    checks = (
        db.query(CheckResult)
        .filter(CheckResult.website_id == website_id)
        .order_by(CheckResult.checked_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "checked_at": c.checked_at,
            "is_up": c.is_up,
            "status_code": c.status_code,
            "response_time": c.response_time,
        }
        for c in checks
    ]
