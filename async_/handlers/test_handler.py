from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from async_.ping_result_dao import PingResultDAO
from time import perf_counter
from sqlalchemy.ext.asyncio import AsyncSession
import async_.ping as p
import aiofiles
from schemas.schemas import PingResultBase


async def async_test(db: AsyncSession):
    dao = PingResultDAO(db)
    
    start = perf_counter()

    async def read_urls() -> list:
        res = []
        async with aiofiles.open("urls.txt", mode="r") as file:
            async for url in file:
                res.append(url.replace("\n", ""))
        return res

    urls = await read_urls()

    ok, failed = await p.async_ping_t(urls=urls)

    result = await dao.create_many_ping_results(ok)
   
    if not result: # if result == None
        res = dict(urls_and_ping_time=[], failed_urls=[], time_spent=[])
        
        for pr in ok:
            res["urls_and_ping_time"].append(dict(url=pr.url, avg_ping_time=pr.avg_ping_time))
        
        for f in failed:
            res["failed_urls"].append(f)
        
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
