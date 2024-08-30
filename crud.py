from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy.exc as exc
import models, schemas
from sqlalchemy import text

def get_ping_results(db: Session) -> list[models.PingResult]: 
    stmt = text("SELECT * FROM pingResult")
    result = db.execute(stmt)
    for row in result:
        pass

    return
    # statement = select(models.PingResult)
    # try:
    #     result = db.execute(statement).all()
    #     for row in result:
    #         print(row)
    # except exc.StatementError:
    #     return exc.StatementError
    # except exc.NoSuchTableError:
    #     return exc.NoSuchTableError
    
    # return result
    
    # TODO refactor to return paginated data

def get_ping_result_by_id(db: Session, record_id: int):
    statement = select(models.PingResult).where(id == record_id)
    # try:
    #     result = db.execute(statement)
    # # except exc.StatementError:
    return


def get_ping_results_by_url(db: Session, url: str):
    return db.query(models.PingResult).where(models.PingResult.url == url).all()

def add_ping_result(db: Session, pr: schemas.PingResultBase):
    record = models.PingResult(url=pr.url, ip=pr.ip, packets_sent=pr.packets_sent, packets_recieved=pr.packets_recieved, avg_ping_time=pr.avg_ping_time, time_sent=pr.time_sent)
    db.add(record)
    db.commit()

def delete_ping_result_by_id(db: Session, record_id):
    recordToDelete = db.get(models.PingResult, record_id)
    db.delete(recordToDelete)
    db.commit()