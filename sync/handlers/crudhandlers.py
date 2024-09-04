from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import sync.ping_result_dao as ping_result_dao
from sqlalchemy.orm import Session
from sync.database import engine
import sqlalchemy.exc as exc

def get_results() -> JSONResponse:
    with Session(engine) as session:
        data = ping_result_dao.get_ping_results(db=session)
        
    if type(data) == dict:
        return JSONResponse(content=jsonable_encoder(data))
    
    return JSONResponse(
        content=jsonable_encoder(data)
    )     

def get_result_by_id(record_id: int) -> JSONResponse:
    with Session(engine) as session:
        data = ping_result_dao.get_ping_result_by_id(db=session, record_id=record_id)
    
    return JSONResponse(content=jsonable_encoder(data))

def get_results_by_url(url: str) -> JSONResponse:
    with Session(engine) as session:
        data = ping_result_dao.get_ping_results_by_url(db=session, url=url)

    if type(data) == dict:
        return JSONResponse(content=jsonable_encoder(data))
   
    return JSONResponse(
        content=jsonable_encoder(data)
    )