from fastapi import Depends, FastAPI, HTTPException
import utils.ping as p
from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/test")
def test(db: Session = Depends(get_db)):
    f = open("urls.txt", "r")
    for url in f:
        res = p.ping(url, 3)
        crud.add_ping_result(db=db, pr=res)
        
@app.get("/a-test")
async def aTest():
    pass