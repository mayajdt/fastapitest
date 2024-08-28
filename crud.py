from sqlalchemy.orm import Session
import models, schemas

def get_ping_results(db: Session):
    return db.query(models.PingResult)
    # TODO refactor to return paginated data

def get_ping_result_by_id(db: Session, record_id:int):
    return db.get(models.PingResult, record_id)

def add_ping_result(db: Session, pr: schemas.PingResultBase):
    record = models.PingResult(url=pr.url, ip=pr.ip, packets_sent=pr.packets_sent, packets_recieved=pr.packets_recieved, avg_ping_time=pr.avg_ping_time, time_sent=pr.time_sent)
    db.add(record)
    db.commit()

def delete_ping_result_by_id(db: Session, record_id):
    recordToDelete = db.get(models.PingResult, record_id)
    db.delete(recordToDelete)
    db.commit()