from fastapi import FastAPI
from app.api.websites import router as websites_router
from app.api.metrics import router as metrics_router
from app.api.alerts import router as alerts_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.db.base import Base
from app.db.session import engine
from app.models.check_result import CheckResult
from app.models.alert_event import AlertEvent
from app.core.config import get_settings
from app.core.scheduler import scheduler, monitor_websites, calculate_all_metrics

app = FastAPI()

app.include_router(websites_router)
app.include_router(metrics_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)
app.include_router(health_router)

@app.on_event("startup")
def startup():
    settings = get_settings()
    if settings.ENV == "production":
        print("Running in production mode")
    Base.metadata.create_all(bind=engine)
    scheduler.add_job(monitor_websites, "interval", seconds=settings.METRICS_INTERVAL_MINUTES * 60)
    scheduler.add_job(calculate_all_metrics, "interval", minutes=settings.METRICS_INTERVAL_MINUTES)
    scheduler.start()
