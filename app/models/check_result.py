from sqlalchemy import Column, Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"), index=True)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Float, nullable=True)
    is_up = Column(Boolean, nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
