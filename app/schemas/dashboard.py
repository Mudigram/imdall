from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WebsiteDashboardItem(BaseModel):
    id: int
    name: str
    url: str

    current_status: str          # "up", "down"
    is_up: bool

    uptime_percentage: float
    avg_response_time_ms: Optional[float]

    last_checked_at: Optional[datetime]
    alert_state: str             # "normal", "warning", "critical"
