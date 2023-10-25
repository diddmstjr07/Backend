from util.sql_es import sql_select # db 데이터를 가져오는 모듈(함수)를 소환
from fastapi import APIRouter

garbage_can = APIRouter(prefix='/garbage_can')

@garbage_can.get("/get")
async def get_db():
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT lat, lng, isFull FROM Garbage_Can_Data")
            return {"kind" : "ok", "data" : response}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1