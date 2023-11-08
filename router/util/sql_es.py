import mysql.connector

db = mysql.connector.connect(
  host="182.211.172.137",
  port="1706",
  user="eunseok07yang",
  password="qwer1234!!",
  database="Drone_Project"
)

def sql_insert(sql):
    try:
        cursor = db.cursor()
        cursor.execute(sql)

        db.commit()

        print("sql insert - complete")
    except:
        print("sql insert - Error : "+sql)

def sql_insert_val(sql, val): # 이게 db에 정보를 넣어줄때 사용하는 함수 
    try:
        cursor = db.cursor() # db랑 연결 
        cursor.execute(sql, val)

        db.commit() # 내용을 저장 

        return {"kind" : "ok", "msg" : "성공"}

        #print("sql insert - complete")
    except: # 에러가 난다면 에러코드를 출력
        print("sql insert - Error : "+sql)
        return {"kind" : "fail", "msg" : "에러", "q": sql, "v": val}

def sql_select(sql): # Server.py 에서 이함수와 통신 (query)를 sql 자리에 대입하여 함수 연산을 진행
    try: # 시도
        cursor = db.cursor() # db 와 통신 
        cursor.execute(sql) # 여기서는 Server.py 에서 전송해준 query를 변수 자리에 대입 -> db와 연결

        # [{key:value},{key:value},{key:value},{key:value},{key:value},{key:value},{key:value}] -> 이 부분의 내부 딕셔너리 부분까지 배열로 전환

        result = cursor.fetchall() # fetchall db에 있는 데이터를 가져오기
        result = list(result) # db에 있는 데이터들을 리스트 형태로 변환하여 reusult에 저장 (업데이트) -> 원래 문자열이 아니였던 경우에만 문자열로 반환

        for a in range(len(result)): #fetchall 결과를 리스트 형태로 변경 -> 이거는 원래 문자열이였던 경우에도 이 위에 문자열 형태를 씌워 문자열로 반환
            result[a] = list(result[a])
        
        return result # db에서 받아온 전보들을 리턴값으로 제시 당연스럽게도 이 부분 또한 다시 Server.py와 통신하여 Server.py의 data라는 변수에 저장 -> 이를 리턴값으로 제시 
    except: # db와 통신이 안되거나, 통신중 문제가 생기는 경우에는 except문을 실행 -> 애러 코드를 출력
        print("sql select - Error : "+sql)

def sql_update(sql):
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

    except:
        print("sql update - Error : "+ sql)

def login_ok(email, password): # Server.py 에서 이함수와 통신 (query)를 sql 자리에 대입하여 함수 연산을 진행
    try: # 시도
        
        cursor = db.cursor() # db 와 통신 
        query = f"SELECT * FROM User_Data WHERE Email = '{email}' and Password = '{password}'" # 이 부분이 
        cursor.execute(query) # 여기서는 Server.py 에서 전송해준 query를 변수 자리에 대입 -> db와 연결

        result = cursor.fetchall() # fetchall db에 있는 데이터를 가져오기
        result = list(result) # db에 있는 데이터들을 리스트 형태로 변환하여 reusult에 저장 (업데이트) -> 원래 문자열이 아니였던 경우에만 문자열로 반환

        for a in range(len(result)): #fetchall 결과를 리스트 형태로 변경 -> 이거는 원래 문자열이였던 경우에도 이 위에 문자열 형태를 씌워 문자열로 반환
            result[a] = list(result[a])
        
        if len(result) > 0:
            return {"kind" : "ok", "msg" : "로그인 성공",  "id" : result[0][0], "name" : result[0][1], "email" : result[0][2]}
        else:
            return {"kind" : "fail", "msg" : "로그인 실패"}
    except: # db와 통신이 안되거나, 통신중 문제가 생기는 경우에는 except문을 실행 -> 애러 코드를 출력
        print("sql insert - Error : " + query)

def select_data(sql): # Server.py 에서 이함수와 통신 (query)를 sql 자리에 대입하여 함수 연산을 진행
    try: # 시도
        cursor = db.cursor() # db 와 통신 
        cursor.execute(sql) # 여기서는 Server.py 에서 전송해준 query를 변수 자리에 대입 -> db와 연결

        result = cursor.fetchall() # fetchall db에 있는 데이터를 가져오기
        result = list(result) # db에 있는 데이터들을 리스트 형태로 변환하여 reusult에 저장 (업데이트) -> 원래 문자열이 아니였던 경우에만 문자열로 반환

        for a in range(len(result)): #fetchall 결과를 리스트 형태로 변경 -> 이거는 원래 문자열이였던 경우에도 이 위에 문자열 형태를 씌워 문자열로 반환
            result[a] = list(result[a])
        
        return result # db에서 받아온 전보들을 리턴값으로 제시 당연스럽게도 이 부분 또한 다시 Server.py와 통신하여 Server.py의 data라는 변수에 저장 -> 이를 리턴값으로 제시 
    except: # db와 통신이 안되거나, 통신중 문제가 생기는 경우에는 except문을 실행 -> 애러 코드를 출력
        print("sql insert - Error : "+sql)

def sql_delete(sql):
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

    except:
        print("sql update - Error : "+ sql)