from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from async_.ping_result_dao import PingResultDAO
import time
from schemas.schemas import PingResultBase
from sqlalchemy.ext.asyncio import AsyncSession

async def async_result_impl(db: AsyncSession) -> JSONResponse:
    dao = PingResultDAO(db)

    result = await dao.get_all_ping_results()

