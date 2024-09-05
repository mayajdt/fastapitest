from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from async_.ping_result_dao import PingResultDAO
from time import perf_counter
from sqlalchemy.ext.asyncio import AsyncSession
import async_.ping as p
import aiofiles
from schemas.schemas import PingResultBase
from itertools import chain

def gen_failed_response_objs(l: chain[tuple]) -> list[dict]:
    res = []
    for el in l:
        res.append(dict(url=el[0], err=el[1]))
    return res

def gen_ok_response_objs(l: list[PingResultBase]) -> list[dict]:
    res = []
    for el in l:
        res.append(
            dict(
                url=el.url,
                avg_ping_time=el.avg_ping_time,
            )
        )
    return res

async def async_test(db: AsyncSession) -> JSONResponse:
    dao = PingResultDAO(db)
    
    start = perf_counter()

    async def read_urls() -> list:
        start = perf_counter()

        res = []
        async with aiofiles.open("urls.txt", mode="r") as file:
            async for url in file:
                res.append(url.replace("\n", ""))

        stop = perf_counter()
        time_spent = stop - start
        print(f'reading files took {time_spent} seconds')

        return res

    urls = await read_urls()

    ok, failed = await p.async_ping_t(urls=urls)

    new_records = p.gen_ping_result_objs(ok)

    result = await dao.create_many_ping_results(new_records)
   
    if not result: # if result == None
        res = dict(urls_and_ping_time=[], failed_urls=[], time_spent=[])
        
        res["urls_and_ping_time"] = gen_ok_response_objs(new_records)
        
        res["failed_urls"] = gen_failed_response_objs(failed)
        
        stop = perf_counter()
        time_spent = stop - start

        res["time_spent"] = time_spent

        return JSONResponse(
            content=jsonable_encoder(res),
            status_code=200
        )
    else:
        return JSONResponse(
            content=jsonable_encoder(result),
            status_code=500
        )        
