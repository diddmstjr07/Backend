from router.util.sql_es import sql_insert_val
import jwt
import datetime

JWT_SECRET = "eunseok07yang"

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