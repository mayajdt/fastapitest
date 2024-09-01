from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import ping, crud, models, time
from schemas import PingResultBase, ErrorResultBase
from sqlalchemy.orm import Session
from database import engine

def construct_response(ok: list, failed: list, time_spent: int):
    res_obj = dict(
        urls_and_ping_time = ok,
        failed_urls = failed,
        time_spent = time_spent,
    )

    res = jsonable_encoder(res_obj)

    return res


def test_impl() -> JSONResponse:
    # start = time.perf_counter()

    # f = open("urls.txt", "r")
    # urls_and_response = []

    # with Session(engine) as session:
    #     for url in f:
    #         ping_res = ping.ping_t(url)

    #         if type(ping_res) == ErrorResultBase:
    #             resp_data = dict(url=ping_res.url, error_name=ping_res.error_name, error_desc=ping_res.error_desc)
    #             resp = jsonable_encoder(resp_data)
    #             return JSONResponse(content=resp, status_code=200)

    #             # urls_and_response.append(dict(url=ping_res.url, error_name=ping_res.error_name, error_desc=ping_res.error_desc))
    #         else:
    #             crud.add_ping_result(db=session, pr=ping_res)
    #             urls_and_response.append(dict(url=ping_res.url, avg_ping_time = ping_res.avg_ping_time))

    # end = time.perf_counter()
    # time_spent = (end - start)

    # return construct_response(urls=urls_and_response, time_spent=time_spent)
    start = time.perf_counter()

    urls = []
    with open("urls.txt", "r") as file:
        for url in file:
            urls.append(url.replace("\n", ""))

    ok, failed = ping.ping_t(urls=urls)
    
    with Session(engine) as session:
        resp = crud.add_bulk_ping_result(db=session, data=ok)

    if not resp:
        res_ok = []
        for el in ok:
            res_frag = dict(url=el.url, avg_ping_time=el.avg_ping_time)
            res_ok.append(res_frag)
        
        stop = time.perf_counter()
        time_spent = stop - start

        return JSONResponse(content=jsonable_encoder(construct_response(ok=res_ok, failed=failed, time_spent=time_spent)))
    else:
        return JSONResponse(content=jsonable_encoder(resp))