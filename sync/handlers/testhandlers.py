from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import sync.ping as p, sync.ping_result_dao as ping_result_dao, time
from schemas.schemas import PingResultBase
from sqlalchemy.orm import Session
from sync.database import engine

def construct_response(ok: list, failed: list, time_spent: int):
    res_obj = dict(
        urls_and_ping_time = ok,
        failed_urls = failed,
        time_spent = time_spent,
    )

    res = jsonable_encoder(res_obj)

    return res


def test_impl() -> JSONResponse:
    start = time.perf_counter()

    urls = []
    with open("urls.txt", "r") as file:
        for url in file:
            urls.append(url.replace("\n", ""))

    ok, failed = p.ping_t(urls=urls)
    
    with Session(engine) as session:
        resp = ping_result_dao.add_bulk_ping_result(db=session, data=ok)

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