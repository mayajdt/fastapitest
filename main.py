from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import test

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/test")
def s_test(db: Session = Depends(get_db)):
    return test.test_impl(db)

@app.post("/a-test")
async def a_test(db: Session = Depends(get_db)):
    return test.test_impl(db)