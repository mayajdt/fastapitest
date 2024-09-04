from fastapi import FastAPI, Depends
import models.models, sync.handlers.testhandlers as synctest, sync.handlers.crudhandlers as synccrud
from sync.database import engine

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from async_.database import get_db
import async_.handlers.test_handler as asynctest, async_.handlers.crud_handlers as asynccrud

models.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# sync endpoints
@app.post("/test")
def s_test():
    return synctest.test_impl()

@app.get("/result")
def result():
    return synccrud.get_results()

@app.get("/result/{record_id}")
def result_by_id(record_id: str):
    record_id_int = int(record_id)
    return synccrud.get_result_by_id(record_id=record_id_int)

@app.get("/result/")
def result_by_url(url: str):
    pass
    

# async endpoints
@app.post("/async-test")
async def async_test(db: AsyncSession = Depends(get_db)):
    await asynctest.async_test(db=db)

@app.get("/async-result")
async def async_result(db: AsyncSession = Depends(get_db)):
    pass

@app.get("/async-result/{record_id}")
async def async_result_by_id(record_id: str, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/async-result/")
async def async_result_by_url(url: str, db: AsyncSession = Depends(get_db)):
    pass