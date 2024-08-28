from pydantic import BaseModel
from datetime import datetime

class PingResultBase(BaseModel):
    url: str
    ip: str
    packets_sent: int
    packets_recieved: int
    avg_ping_time: float
    time_sent: datetime