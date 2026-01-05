from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.website import Website
from app.models.check_result import CheckResult
from app.services.website_checker import run_website_check
from app.services.metrics import calculate_metrics

scheduler = BackgroundScheduler()

def monitor_websites():
    """
    Check all active websites using the website_checker service.
    The service handles HTTP checks, metrics calculation, and alert evaluation.
    """
    db: Session = SessionLocal()

    try:
        websites = (
            db.query(Website)
            .filter(Website.is_active == True)
            .all()
        )

        for website in websites:
            run_website_check(db, website)
    finally:
        db.close()

def calculate_all_metrics():
    db = SessionLocal()
    try:
        website_ids = (
            db.query(CheckResult.website_id)
            .distinct()
            .all()
        )

        for (website_id,) in website_ids:
            calculate_metrics(db, website_id, hours=24)
    finally:
        db.close()
