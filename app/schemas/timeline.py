from pydantic import BaseModel
from datetime import datetime


class TimelinePoint(BaseModel):
    timestamp: datetime
    value: float
