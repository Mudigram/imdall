from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class WebsiteMetrics(Base):
    __tablename__ = "website_metrics"

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"), index=True)

    uptime_percentage = Column(Float, nullable=False)
    avg_response_time = Column(Float, nullable=True)

    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)

    consecutive_failures = Column(Integer, default=0)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
