from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy.exc as exc
from sqlalchemy import text, insert
from models import PingResult
from schemas import PingResultBase

def get_ping_results(db: Session) -> list[dict] | dict:
    '''
    Will attempt to fetch all records from PingResult.

    If successful, function will return list[dict]

    If not, function will return following dict object:

        dict(
            error_name,
            error_desc
        )
    '''
    try:
        res = db.execute(select(PingResult))
    except Exception as err:
        return dict(error_name= err.__class__.__name__, error_desc="Couldn't fetch ping results, check logs")
    else:
        ret = []
        for r in res:
            ret.append(r._asdict())
        return ret

def get_ping_result_by_id(db: Session, record_id: int) -> dict:
    '''
    Will attempt to fetch a single record by its id from database.

    If successful, function will return a dict with the record data

    If not, function will return following dict object:

        dict(
            error_name,
            error_desc
        )
    '''
    record = db.get(PingResult, record_id)
    if not record:
        return dict(
            error_name="NoRecordFound",
            error_desc="No record found in database"
        )
    return record.__dict__


def get_ping_results_by_url(db: Session, url: str) -> list[dict] | dict:
    '''
    Will attempt to fetch a list of records filtered by url.

    If successful, function will return a list of dicts with the record data

    If not, function will return following dict object:

        dict(
            error_name,
            error_desc
        )
    '''
    try:
         res = db.execute(
            select(PingResult).
            where(PingResult.url == url)
        )
    except Exception as err:
        return dict(error_name= err.__class__.__name__, error_desc="Couldn't fetch ping results, check logs")
    else:
        ret = []
        for r in res:
            ret.append(r._asdict())
        return ret

def add_ping_result(db: Session, data: PingResult) -> None | dict:
    '''
    Will attempt to persist a single record to database.

    If successful, function will return None

    If not, function will return following dict object:

        dict(
            error_name,
            error_desc
        )
    '''
    try:
        db.add(data)
        db.commit()
    except Exception as err:
        return dict(error_name= err.__class__.__name__, error_desc="Couldn't bulk insert ping results, check logs")
    else:
        return None

def add_bulk_ping_result(db: Session, data: list[PingResultBase]) -> None | dict:
    '''
    Will attempt to persist a bulk of records to database.

    If successful, function will return None

    If not, function will return following dict object:

        dict(
            error_name,
            error_desc
        )
    '''
    records = []
    for d in data:
        records.append(d.model_dump())
    try:
        db.execute(
            insert(PingResult),
            records
        )
    except Exception as err:
        return dict(error_name= err.__class__.__name__, error_desc="Couldn't bulk insert ping results, check logs")
    else:
        db.commit()
        return None
    
def delete_ping_result_by_id(db: Session, record_id) -> None | dict:
    '''
    Will attempt to delete a single record from database by id.

    If successful, function will return None

    If not, function will return following dict object:

        dict(
            error_name,
            error_desc
        )
    '''
    try:
        recordToDelete = db.get(PingResult, record_id)
        db.delete(recordToDelete)
        db.commit()
    except Exception as err:
        return dict(error_name= err.__class__.__name__, error_desc="Couldn't delete ping results, check logs")
    else:
        return None