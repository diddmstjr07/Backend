import router.util.sql_es as q
from fastapi import APIRouter
from  pydantic import BaseModel

garbage = APIRouter(prefix='/garbage')

@garbage.get("/get", tags=['garbage'])
async def get_db():
    err_cnts = 1
    my_lat = '35.12461879' 
    my_lng= '126.9235712'
    km_range = '1' #미터 단위
    while True:
        try:
            response = q.sql_select(f"SELECT id, lat, lng, datetime, object, object, conf, image FROM Garbage_Data WHERE com = 'N'")
            # response = sql_select(f"SELECT id, lat, lng, datetime, object, object, conf, image, ST_Distance_Sphere(POINT('{my_lng}', '{my_lat}'), POINT(lng, lat)) AS distance FROM Garbage_Data WHERE ST_Distance_Sphere(POINT('{my_lng}', '{my_lat}'), POINT(lng, lat)) <= {km_range} ORDER BY distance ASC")
            
            return {"kind" : "ok", "data" : response}
        
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1

class upload(BaseModel):
    lat: str | None = None
    lng: str | None = None
    datetime: str | None = None
    object: str | None = None
    conf: str | None = None
    img: str | None = None

@garbage.post("/upload", tags=['garbage'])
async def upload_data(upload_: upload):
    print(upload_)
    err_cnt = 1
    query = "INSERT INTO `Garbage_Data` (`lat`, `lng`, `datetime`, `object`, `conf`, `image`) VALUES (%s, %s, %s, %s, %s, %s)"
    # 쿼리문을 작성하여 테이블에 요소 넣기
    while True:
        try:
            val = (upload_.lat, upload_.lng, upload_.datetime, upload_.object, upload_.conf, upload_.img) # 쿼리문에 있는 %s 데이터를 차례차례 data 배열이 받아줌
            return q.sql_insert_val(query, val) # query, val을 sql_es.py 파일로 전송
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnt > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "쿼리 에러"}
            err_cnt += 1
