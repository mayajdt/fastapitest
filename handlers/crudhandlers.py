from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import ping, crud, models, time
from schemas import PingResultBase, ErrorResultBase
from sqlalchemy.orm import Session
from database import engine
import sqlalchemy.exc as exc

def construct_many_results_response(data: PingResultBase):
    resp = []
    for d in data:
        resp_frag = PingResultBase(d)
        resp.append(resp_frag)

    return resp

def construct_error_response(error_name: str, error_desc: str):
    resp_obj = dict(
        error_name = error_name,
        error_desc = error_desc
    )

    return jsonable_encoder(resp_obj)

def get_results() -> JSONResponse:
    resp = None
    with Session(engine) as session:
        try:
            data = crud.get_ping_results(db=session)
        except exc.StatementError:
            resp = construct_error_response(error_name=exc.StatementError.__name__, error_desc="Something went wrong when executing the SQL statement")
        except exc.NoSuchTableError:
            resp = construct_error_response(error_name=exc.NoSuchTableError.__name__, error_desc="Table does not exist")
        else:
            resp = construct_many_results_response(data=data)

    return JSONResponse(content=resp)

def get_result_by_id(record_id: int) -> JSONResponse:
    with Session(engine) as session:
        data = crud.get_ping_result_by_id(db=session, record_id=record_id)
    
    resp = PingResultBase(data).model_dump()

    return JSONResponse(content=jsonable_encoder(resp))

def get_results_by_url(url: str) -> JSONResponse:
    with Session(engine) as session:
        data = crud.get_ping_results_by_url(db=session, url=url)
    
    resp = construct_many_results_response(data=data)

    return JSONResponse(content=resp)