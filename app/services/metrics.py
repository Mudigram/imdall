from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.check_result import CheckResult
from app.models.website_metrics import WebsiteMetrics

def calculate_metrics(
    db: Session,
    website_id: int,
    hours: int = 24
):
    window_end = datetime.utcnow()
    window_start = window_end - timedelta(hours=hours)

    checks = (
        db.query(CheckResult)
        .filter(
            CheckResult.website_id == website_id,
            CheckResult.checked_at >= window_start
        )
        .all()
    )

    if not checks:
        return None

    total = len(checks)
    up = sum(1 for c in checks if c.is_up)
    avg_response = (
        sum(c.response_time for c in checks if c.response_time)
        / max(1, sum(1 for c in checks if c.response_time))
    )
    
    # Calculate consecutive failures from most recent checks
    consecutive_failures = 0
    recent_checks = sorted(checks, key=lambda c: c.checked_at, reverse=True)
    for check in recent_checks:
        if not check.is_up:
            consecutive_failures += 1
        else:
            break  # Stop counting when we hit a successful check

    metrics = WebsiteMetrics(
        website_id=website_id,
        uptime_percentage=(up / total) * 100,
        avg_response_time=avg_response,
        consecutive_failures=consecutive_failures,
        window_start=window_start,
        window_end=window_end
    )

    db.add(metrics)
    db.commit()
    return metrics
