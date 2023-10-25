from fastapi import FastAPI, UploadFile # fastip를 호출하는 모듈
from util.sql_es import sql_select # db 데이터를 가져오는 모듈(함수)를 소환
from pydantic import BaseModel
from util.sql_es import sql_insert_val
from util.sql_es import login_ok
from util.sql_es import select_data
from util.sql_es import sql_update
from util.sql_es import sql_delete
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import jwt
import datetime

app = FastAPI() #fastip 모듈을 변수에 저장

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Server_port"}