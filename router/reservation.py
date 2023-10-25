from fastapi import APIRouter
import router.util.sql_es as q  # db 데이터를 가져오는 모듈(함수)를 소환
from pydantic import BaseModel

reservation = APIRouter(prefix='/reservation')

class Reservation(BaseModel):
    Token: str | None = None
    Uid: str | None = None

@reservation.post("/reservation", tags=['reservation'])
async def get_res(data: Reservation):
    err_cnts = 1
    while True:
        try:
            response = q.sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            response_select = q.sql_select(f"SELECT res FROM Garbage_Data WHERE id = '{data.Uid}'")
            if response_select[0][0] == None:
                response_main = q.sql_update(f"UPDATE Garbage_Data SET res = '{response[0][0]}' WHERE id = '{data.Uid}'")
                return {"kind" : "ok", "data" : response_main}
            else:
                return {"kind" : "ok_resed", "data" : response_select}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1

class Reservation_show(BaseModel):
    Token: str | None = None

@reservation.post("/reservation_show", tags=['reservation'])
async def get_res(data: Reservation_show):
    err_cnts = 1
    while True:
        try:
            response = q.sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = q.sql_select(f"SELECT id, lat, lng, datetime, object, conf, image FROM Garbage_Data WHERE res = '{response[0][0]}' and com = 'N'")
            return {"kind" : "ok_resed", "data" : responses}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1


class Reservation_res(BaseModel):
    Token: str | None = None

@reservation.post("/submit", tags=['reservation'])
async def reserve(data: Reservation_res):
    err_cnts = 1
    while True:
        try:
            response = q.sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses =q.sql_select(f"SELECT id FROM Garbage_Data WHERE res = '{response[0][0]}' and com = 'N'")
            extracted_elements = [sublist[0] for sublist in responses[:3]]
            for numbers in extracted_elements:
                re_response = q.sql_update(f"UPDATE Garbage_Data SET com = 'Y'  WHERE id = {numbers}")
            return {"kind" : "ok", 'data' : re_response}
        except:
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB error"}
            
class Display(BaseModel):
    Token: str | None = None

@reservation.post("/display", tags=['reservation'])
async def reserve(data: Display):
    err_cnts = 1
    while True:
        try:
            response = q.sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = q.sql_select(f"SELECT id, lat, lng, datetime, object, conf, image FROM Garbage_Data WHERE res = '{response[0][0]}' and com = 'Y'")
            return {"kind" : "ok", 'data' : responses}
        except:
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB error"}