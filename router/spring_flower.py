import router.util.sql_es as q
from fastapi import APIRouter
from  pydantic import BaseModel

flower = APIRouter(prefix='/flower')

class upload(BaseModel):
    lat: str | None = None
    lng: str | None = None

@flower.post("/upload", tags=['flower'])
async def upload_data(upload_: upload):
    print(upload_)
    err_cnt = 1
    query = "INSERT INTO `Spring_Flower` (`lat`, `lng`) VALUES (%s, %s)"
    # 쿼리문을 작성하여 테이블에 요소 넣기
    while True:
        try:
            val = (upload_.lat, upload_.lng) # 쿼리문에 있는 %s 데이터를 차례차례 data 배열이 받아줌
            return q.sql_insert_val(query, val) # query, val을 sql_es.py 파일로 전송
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnt > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "쿼리 에러"}
            err_cnt += 1

@flower.get("/get", tags=['flower'])
async def get_db():
    err_cnts = 1
    while True:
        try:
            response = q.sql_select(f"SELECT id, lat, lng FROM Spring_Flower")            
            return {"kind" : "ok", "data" : response}
        
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}