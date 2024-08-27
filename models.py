from sqlalchemy import Column, Integer, String, DateTime

from database import Base  

class PingResult(Base):
    __tablename__ = "pingResults"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    ip = Column(String)
    packets_sent = Column(Integer)
    packets_recieved = Column(Integer)
    time_spent = Column(Integer)
    time_sent = Column(DateTime)