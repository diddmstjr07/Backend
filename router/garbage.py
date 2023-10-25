import router.util.sql_es as q
from fastapi import APIRouter

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
