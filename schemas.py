from pydantic import BaseModel
from datetime import datetime

class PingResultBase(BaseModel):
    url: str
    ip: str
    packets_sent: int
    packets_recieved: int
    time_spent: int
    time_sent: datetime