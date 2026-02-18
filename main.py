from fastapi import FastAPI
from app.utils.constants import MESSAGES
from app.db.database import engine
from app.db.base import Base

app = FastAPI(title='ERP API')

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return MESSAGES['API_RUNNING']