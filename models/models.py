from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import DeclarativeBase
from schemas.schemas import PingResultBase
from sqlalchemy import ColumnElement

class Base(DeclarativeBase):
    pass

class PingResult(Base):
    __tablename__ = "pingResults"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    ip = Column(String)
    packets_sent = Column(Integer)
    packets_recieved = Column(Integer)
    avg_ping_time = Column(Float)
    time_sent = Column(DateTime)