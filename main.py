from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models, handlers.testhandlers as test, handlers.crudhandlers as crud
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/test")
def s_test():
    return test.test_impl()

@app.post("/a-test")
async def a_test():
    return test.test_impl()

@app.get("/result")
def result():
    return crud.get_results()

@app.get("/result/{record_id}")
def result_by_id(record_id: str):
    record_id_int = int(record_id)
    return crud.get_result_by_id(record_id=record_id_int)

@app.get("/result/")
def result_by_url(url: str):
    return crud.get_results_by_url(url=url)