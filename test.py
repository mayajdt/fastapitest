from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import ping as p
from schemas import PingResultBase, ErrorResultBase
from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal
import time

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def construct_response(urls: list, time_spent: int) -> JSONResponse:
    res_obj = dict(
        urls_and_ping_time = urls,
        time_spent = time_spent,
    )

    res = jsonable_encoder(res_obj)

    return res


def test_impl(db: Session) -> JSONResponse:
    start = time.perf_counter()

    f = open("urls.txt", "r")
    urls_and_response = []
    for url in f:
        ping_res = p.ping_t(url)
        if type(ping_res) == ErrorResultBase:
            resp_data = dict(url=ping_res.url, error_name=ping_res.error_name, error_desc=ping_res.error_desc)
            resp = jsonable_encoder(resp_data)
            return JSONResponse(content=resp, status_code=200)

            # urls_and_response.append(dict(url=ping_res.url, error_name=ping_res.error_name, error_desc=ping_res.error_desc))
        else:
            crud.add_ping_result(db=db, pr=ping_res)
            urls_and_response.append(dict(url=ping_res.url, avg_ping_time = ping_res.avg_ping_time))

    end = time.perf_counter()
    time_spent = (end - start)

    return construct_response(urls=urls_and_response, time_spent=time_spent)