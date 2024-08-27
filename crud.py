from sqlalchemy.orm import Session
import models, schemas

def get_ping_result(db: Session, result_id:int):
    return db.query(models.PingResult).filter(models.PingResult.id == result_id)

def add_ping_result(db: Session, pr: schemas.PingResultBase):
    record = models.PingResult(url=pr.url, ip=pr.ip, packets_sent=pr.packets_sent, packets_recieved=pr.packets_recieved, time_spent=pr.time_spent, time_sent=pr.time_sent)
    db.add(record)
    db.commit()
    db.refresh(record)
