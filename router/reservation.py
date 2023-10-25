from fastapi import APIRouter
from util.sql_es import sql_select # db 데이터를 가져오는 모듈(함수)를 소환
from pydantic import BaseModel
from util.sql_es import sql_insert_val
from util.sql_es import login_ok
from util.sql_es import select_data
from util.sql_es import sql_update
from util.sql_es import sql_delete

reservation = APIRouter(prefix='/user')

class Reservation(BaseModel):
    Token: str | None = None
    Uid: str | None = None

@reservation.post("/reservation")
async def get_res(data: Reservation):
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            response_select = sql_select(f"SELECT res FROM Garbage_Data WHERE id = '{data.Uid}'")
            if response_select[0][0] == None:
                response_main = sql_update(f"UPDATE Garbage_Data SET res = '{response[0][0]}' WHERE id = '{data.Uid}'")
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

@reservation.post("/reservation_show")
async def get_res(data: Reservation_show):
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = sql_select(f"SELECT id, lat, lng, datetime, object, conf, image FROM Garbage_Data WHERE res = '{response[0][0]}' and com = 'N'")
            return {"kind" : "ok_resed", "data" : responses}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1


class Reservation_res(BaseModel):
    Token: str | None = None

@reservation.post("/submit")
async def reserve(data: Reservation_res):
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = sql_select(f"SELECT id FROM Garbage_Data WHERE res = '{response[0][0]}' and com = 'N'")
            extracted_elements = [sublist[0] for sublist in responses[:3]]
            for numbers in extracted_elements:
                re_response = sql_update(f"UPDATE Garbage_Data SET com = 'Y'  WHERE id = {numbers}")
            return {"kind" : "ok", 'data' : re_response}
        except:
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB error"}
            
class Display(BaseModel):
    Token: str | None = None

@reservation.post("/display")
async def reserve(data: Display):
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = sql_select(f"SELECT id, lat, lng, datetime, object, conf, image FROM Garbage_Data WHERE res = '{response[0][0]}' and com = 'Y'")
            return {"kind" : "ok", 'data' : responses}
        except:
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB error"}