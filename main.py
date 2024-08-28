from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import ping as p
from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal, engine
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def construct_response(urls: list, timeSpent: int) -> JSONResponse:
    resObj = dict(
        urls_and_ping_time = urls,
        time_spent = timeSpent,
    )

    res = jsonable_encoder(resObj)

    return res


@app.post("/test")
def test(db: Session = Depends(get_db)):
    start = time.time()

    f = open("urls.txt", "r")
    urlsAndPingTimes = []
    for url in f:
        pingRes = p.ping(url)
        crud.add_ping_result(db=db, pr=pingRes)
        urlsAndPingTimes.append(dict(url=pingRes.url, avgPingTime = pingRes.avg_ping_time))

    end = time.time()
    timeSpent = (end - start)

    res = construct_response(urls=urlsAndPingTimes, timeSpent=timeSpent)

    return JSONResponse(content=res)
  
@app.get("/a-test")
async def aTest():
    start = time.time()

    f = open("urls.txt", "r")
    urlsAndPingTimes = []
    for url in f:
        pingRes = p.ping()