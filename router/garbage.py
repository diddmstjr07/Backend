from fastapi import FastAPI, UploadFile # fastip를 호출하는 모듈
from util.sql_es import sql_select # db 데이터를 가져오는 모듈(함수)를 소환
from pydantic import BaseModel
from util.sql_es import sql_insert_val
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

garbage = APIRouter(prefix='/garbage')

@garbage.get("/get")
async def get_db():
    err_cnts = 1
    my_lat = '35.12461879' 
    my_lng= '126.9235712'
    km_range = '1' #미터 단위
    while True:
        try:
            response = sql_select(f"SELECT id, lat, lng, datetime, object, object, conf, image FROM Garbage_Data WHERE com = 'N'")
            # response = sql_select(f"SELECT id, lat, lng, datetime, object, object, conf, image, ST_Distance_Sphere(POINT('{my_lng}', '{my_lat}'), POINT(lng, lat)) AS distance FROM Garbage_Data WHERE ST_Distance_Sphere(POINT('{my_lng}', '{my_lat}'), POINT(lng, lat)) <= {km_range} ORDER BY distance ASC")
            
            return {"kind" : "ok", "data" : response}
        
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1
