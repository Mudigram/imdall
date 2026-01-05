from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"))

    alert_type = Column(String)  # "downtime" | "performance"
    severity = Column(String)    # "warning" | "critical"
    message = Column(String)

    triggered_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)