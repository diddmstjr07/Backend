from fastapi import APIRouter
from util.sql_es import sql_select # db 데이터를 가져오는 모듈(함수)를 소환
from pydantic import BaseModel
from util.sql_es import sql_insert_val
from util.sql_es import login_ok
from util.sql_es import select_data
from util.sql_es import sql_update
from util.sql_es import sql_delete

user = APIRouter(prefix='/user')

class User(BaseModel):
    First_name: str | None = None
    Email: str | None = None
    Password: str | None = None

@user.post("/Register")
async def create_item(item: User):
    print(item)
    err_cnt = 1
    query = "INSERT INTO `User_Data` (`First_name`, `Email`, `Password`) VALUES (%s, %s, %s)"
    # 쿼리문을 작성하여 테이블에 요소 넣기
    while True:
        try:
            val = (item.First_name,item.Email,item.Password) # 쿼리문에 있는 %s 데이터를 차례차례 data 배열이 받아줌
            return sql_insert_val(query, val) # query, val을 sql_es.py 파일로 전송
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnt > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "쿼리 에러"}
            err_cnt += 1

class UserLogin(BaseModel):

    Email: str | None = None
    Password: str | None = None

@user.post("/Login")
async def check_item(data : UserLogin):
    err_cnts = 1
    while True:
        try:
            res = login_ok(data.Email, data.Password)
            if res["kind"] == "ok":
                token_res = NewToken(res["id"])
                if token_res["kind"] == "ok" :
                    return {"kind" : "ok", "msg" : "로그인 성공",  
                            "token" : token_res["token"], "name" : res["name"], "email" : res["email"]}
            return {"kind" : "fail", "msg" : "로그인 실패"}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                break
            err_cnts += 1

class update(BaseModel):
    Name: str | None =  None
    Password: str | None = None
    Token: str | None = None

@user.post("/Update")
async def updated(data: update):
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = sql_update(f"UPDATE User_Data SET First_name = '{data.Name}' , Password = '{data.Password}' WHERE id = '{response[0][0]}'")

            return {"kind" : "ok", "data" : responses}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1

class delete(BaseModel):
    Id: int | None = None

@user.post("/deletedb")
async def delete_db(data: delete):
    err_cnts = 1
    while True:
        try:
            response = sql_delete(f"DELETE FROM User_Data WHERE id = {data.Id}")
            return {"kind" : "ok", "data" : response}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1

class Privacy(BaseModel):
    Token: str | None = None

@user.post("/privacy")
async def privacy_page(data: Privacy):
    err_cnts = 1
    while True:
        try:
            response = select_data(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            responses = select_data(f"SELECT * FROM User_Data WHERE id = {response[0][0]}")
            return {"kind" : "ok", 'data' : responses}
        except:
            if err_cnts > 5:
                print('error - id : ')
                break
            err_cnts += 1

class get(BaseModel):
    Token: str | None = None

@user.post("/getid")
async def get_db(data: get):
    err_cnts = 1
    while True:
        try:
            response = sql_select(f"SELECT uid FROM Session WHERE AccessToken = '{data.Token}'")
            response_main = sql_select(f"SELECT First_name FROM User_Data WHERE id = {response[0][0]}")
            return {"kind" : "ok", "data" : response_main}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1