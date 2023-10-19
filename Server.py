from fastapi import FastAPI, UploadFile # fastip를 호출하는 모듈
from sql_es import sql_select # db 데이터를 가져오는 모듈(함수)를 소환
from pydantic import BaseModel
from sql_es import sql_insert_val
from sql_es import login_ok
from sql_es import select_data
from sql_es import sql_update
from sql_es import sql_delete
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import jwt
import datetime

JWT_SECRET = "eunseok07yang"
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
    return {"message": "Hello World"}

class upload(BaseModel):
    lat: str | None = None
    lng: str | None = None
    datetime: str | None = None
    object: str | None = None
    conf: str | None = None
    img: str | None = None

@app.post("/upload/garbage")
async def upload_data(upload_: upload):
    print(upload_)
    err_cnt = 1
    query = "INSERT INTO `Garbage_Data` (`lat`, `lng`, `datetime`, `object`, `conf`, `image`) VALUES (%s, %s, %s, %s, %s, %s)"
    # 쿼리문을 작성하여 테이블에 요소 넣기
    while True:
        try:
            val = (upload_.lat, upload_.lng, upload_.datetime, upload_.object, upload_.conf, upload_.img) # 쿼리문에 있는 %s 데이터를 차례차례 data 배열이 받아줌
            return sql_insert_val(query, val) # query, val을 sql_es.py 파일로 전송
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnt > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "쿼리 에러"}
            err_cnt += 1

@app.get("/items/{item_id}")
async def item(item_id):
    return{"item_id": item_id}

@app.get("/item/{item_id}")
async def item(item_id):
    return{"item_id": item_id}

fake_items_db = [{'item_name' : 'Foo'}, {'item_name' : 'Bar'}, {'item_name' : 'Baz'}]

@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get('/getdb/{id}') # 주소창을 선언 (address를 열어줌)
async def get_db(id): # 함수를 이용하여 get_db 라는 함수를 만들어주고, 매개변수인 id를 선언
    query = f'select * from CCTV_Data where id = {id}' #  쿼리문을 작성, select *(전체를 선택) from ~~ (이 테이블에 대한) where ~~ (테이블 요소 중 필드 요소 중 선택을 함)
    data = sql_select(query) # 이렇게 필터링 된 쿼리 요소를 함수 sql_select에 담아 다른 시트로 전송하여 함수에 맞춰 형성된 자신이 원하는 데이터를 data에 저장 
    return data # data 값을 return

class User(BaseModel):
    First_name: str | None = None
    Email: str | None = None
    Password: str | None = None

@app.post("/Register")
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

@app.get("/Check_data/{id}")
async def check_data(id:str):
    err_cnts = 1
    query = f"SELECT * FROM User_Data WHERE id = {id}"
    while True:
        try:
            msg = select_data(query)
            if len(msg) == 1:
                return {"kind" : "ok", "msg" : msg}
            else:
                return {"kind" : "fail", "msg" : "비정상적인 접근입니다"}
        except:
            if err_cnts > 5:
                print('error - id : ')
                break
            err_cnts += 1

@app.post("/photo")
async def upload_photo(file: UploadFile):
    UPLOAD_DIR = "/var/www/html/photo"

    content = await file.read()
    filename = f"{str(uuid.uuid4())}.jpg"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)
        
    return {"filename": filename}


@app.get("/getDB")
async def get_db():
    err_cnts = 1
    my_lng = '126.9080369'
    my_lat = '35.12461879'
    km_range = '1' #미터 단위
    while True:
        try:
            # response = sql_select(f"SELECT id, lat, lng, datetime, object, object, conf, image FROM Garbage_Data")
            response = sql_select(f"SELECT id, lat, lng, datetime, object, object, conf, image, ST_Distance_Sphere(POINT('{my_lng}', '{my_lat}'), POINT(lng, lat)) AS distance FROM Garbage_Data WHERE ST_Distance_Sphere(POINT('{my_lng}', '{my_lat}'), POINT(lng, lat)) <= {km_range} ORDER BY distance ASC")
            
            return {"kind" : "ok", "data" : response}
        
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1

class update(BaseModel):
    Name: str | None =  None
    Password: str | None = None
    Id: int | None = None

@app.post("/Update")
async def updated(data: update):
    err_cnts = 1
    while True:
        try:
            response = sql_update(f"UPDATE User_Data SET First_name = '{data.Name}' , Password = '{data.Password}' WHERE id = {data.Id}")
            return {"kind" : "ok", "data" : response}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnts > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "DB ERROR"}
            err_cnts += 1

class get(BaseModel):
    Token: str | None = None

@app.post("/getid")
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

@app.get("/getDb")
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

class delete(BaseModel):
    Id: int | None = None

@app.post("/deletedb")
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

def NewToken(uid: int):
    token = jwt.encode({"user_id":uid}, JWT_SECRET, algorithm="HS256")
    expires = datetime.datetime.now() + datetime.timedelta(days=30)

    query = "INSERT INTO `Session` (`AccessToken`, `uid`, `expires`) VALUES (%s, %s, %s)"
    val = (token, uid, expires)

    # 쿼리문을 작성하여 테이블에 요소 넣기
    while True:
        try:
            res = sql_insert_val(query, val) # query, val을 sql_es.py 파일로 전송
            if res["kind"] == "ok":
                return {"kind" : "ok", "token" : token}
            return {"kind" : "fail"}
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnt > 5:
                print('error - id : ')
                return {"kind" : "fail", "msg" : "쿼리 에러"}
            err_cnt += 1

class UserLogin(BaseModel):

    Email: str | None = None
    Password: str | None = None

@app.post("/Login")
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