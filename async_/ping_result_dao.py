from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import PingResult
from schemas.schemas import PingResultBase
import time

class PingResultDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_ping_result_by_id(self, record_id: int) -> dict | None:
        try:
            result = await self.session.execute(
                select(PingResult).
                where(PingResult.id == record_id)
            )
        except Exception as err:
            return dict(
                error_name= err.__class__.__name__, 
                error_desc="Couldn't fetch ping resul, check logs"
            )
        else:
            record = result.scalars().first()
            if not record:
                return dict(
                    error_name="NoRecordFound",
                    error_desc="No record found in database"
                )
            return record.__dict__
    
    async def get_all_ping_results(self) -> list[dict]:
        try:
            result = await self.session.execute(select(PingResult))
        except Exception as err:
            return dict(
                error_name= err.__class__.__name__, 
                error_desc="Couldn't fetch ping result, check logs"
            )
        else:
            records = result.scalars().all()
            if len(records) == 0:
                return dict(
                    error_name="NoRecordFound",
                    error_desc="No record found in database"
                )
            return records

    async def get_ping_result_by_url(self, url: str) -> list[dict] | dict:
        try:
            result = await self.session.execute(
                select(PingResult).
                where(PingResult.url == url)
            )
        except Exception as err:
            return dict(
                error_name= err.__class__.__name__, 
                error_desc="Couldn't fetch ping results, check logs"
            )
        else:
            records = result.scalars().all()
            if len(records) == 0:
                return dict(
                    error_name="NoRecordFound",
                    error_desc="No record found in database"
                )
            
            return records

    async def create_ping_result(self, pr_data: PingResultBase) -> None | dict:
        record = PingResult(**pr_data.model_dump())
        try:
            self.session.add(record)
        except Exception as err:
            await self.session.rollback()
            return dict(
                error_name= err.__class__.__name__, 
                error_desc="Couldn't insert ping result, check logs"
            )
        else:
            await self.session.commit()

    async def create_many_ping_results(self, ping_result_list: list[PingResultBase]) -> None | dict:
        start = time.perf_counter()

        records = []
        for pr in ping_result_list:
            records.append(PingResult(**pr.model_dump()))

        try:
            self.session.add_all(records)
        except Exception as err:
            await self.session.rollback()
            return dict(
                error_name= err.__class__.__name__, 
                error_desc="Couldn't bulk insert ping results, check logs"
            )
        else:
            stop = time.perf_counter()
            time_spent = stop - start
            print(f'persisting records took {time_spent} seconds')

            await self.session.commit()

    async def delete_ping_result_by_id(self, record_id: int) -> None | dict:
        try:
            record = await self.session.get(PingResult, record_id)
        except Exception as err:
            return dict(
                error_name= err.__class__.__name__, 
                error_desc="Couldn't fetch  ping result object from database, check logs"
            )
        else:
            if not record:
                return dict(
                        error_name="NoRecordFound",
                        error_desc="No record found in database"
                )
            try:
                await self.session.delete(record)
            except Exception as err:
                await self.session.rollback()
                return dict(
                    error_name= err.__class__.__name__, 
                    error_desc="Couldn't delete ping result object, check logs"
                )
            else:
                await self.session.commit()