import logging
from sqlalchemy.orm import Session
from app.models.website import Website
from app.models.check_result import CheckResult
from app.models.website_metrics import WebsiteMetrics
from app.core.checker import check_website
from app.services.metrics import calculate_metrics
from app.services.alert_helpers import trigger_alert_if_needed, resolve_alert_if_needed

logger = logging.getLogger(__name__)


def run_website_check(db: Session, website: Website):
    """
    Orchestrates a complete website check cycle:
    1. Perform HTTP check
    2. Save check result
    3. Calculate metrics
    4. Evaluate alerts (trigger/resolve)
    
    Returns the created CheckResult instance.
    """
    try:
        logger.info(f"Checking website: {website.url}")
        
        # 1. Perform HTTP check
        result = check_website(website.url)
        
        # 2. Save check result
        check = CheckResult(
            website_id=website.id,
            status_code=result["status_code"],
            response_time=result["response_time"],
            is_up=result["is_up"]
        )
        db.add(check)
        db.flush()  # Get the check ID without committing yet
        
        # 3. Calculate metrics
        metrics = compute_metrics(db, website.id)
        
        # 4. Evaluate and trigger/resolve alerts
        if metrics:
            evaluate_alerts(db, website, metrics)
        
        db.commit()
        logger.info(f"✓ Check completed for {website.url}")
        return check
        
    except Exception as e:
        logger.error(f"✗ Check failed for {website.url}: {e}")
        db.rollback()
        raise


def compute_metrics(db: Session, website_id: int, hours: int = 24) -> WebsiteMetrics | None:
    """
    Calculate and save metrics for a website.
    Returns the calculated WebsiteMetrics or None if no checks exist.
    """
    return calculate_metrics(db, website_id, hours)


def evaluate_alerts(db: Session, website: Website, metrics: WebsiteMetrics):
    """
    Evaluate metrics and trigger/resolve alerts based on thresholds.
    
    Alert types:
    - downtime: Triggered when consecutive_failures >= 5
    - performance: Triggered when avg_response_time_ms > 2000
    """
    
    # Convert response time to milliseconds if it exists
    avg_response_time_ms = None
    if metrics.avg_response_time is not None:
        avg_response_time_ms = metrics.avg_response_time * 1000
    
    # --- Downtime Alert Logic ---
    if metrics.consecutive_failures >= 5:
        trigger_alert_if_needed(
            db,
            website.id,
            "downtime",
            f"{website.name} is down ({metrics.consecutive_failures} consecutive failures)"
        )
    else:
        # Resolve downtime alert if site is back up
        resolve_alert_if_needed(
            db,
            website.id,
            "downtime"
        )
    
    # --- Performance Alert Logic ---
    if avg_response_time_ms is not None and avg_response_time_ms > 2000:
        trigger_alert_if_needed(
            db,
            website.id,
            "performance",
            f"{website.name} has high response time ({avg_response_time_ms:.0f}ms)"
        )
    elif avg_response_time_ms is not None and avg_response_time_ms <= 2000:
        # Resolve performance alert if response time is back to normal
        resolve_alert_if_needed(
            db,
            website.id,
            "performance"
        )
