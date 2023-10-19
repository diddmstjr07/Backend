from sql_es import sql_insert_val

def upload_db(data):
    err_cnt = 1
    query = "INSERT INTO `CCTV_Data` (`manage_organ`, `address_num`, `address_road`, `cnt`, `pixel`, `angle`, `save_day`, `install_year`, `lat`, `lng`, `insert_info`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # 쿼리문을 작성하여 테이블에 요소 넣기
    while True:
        try:
            val = (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10], data[11]) # 쿼리문에 있는 %s 데이터를 차례차례 data 배열이 받아줌
            sql_insert_val(query, val) # query, val을 sql_es.py 파일로 전송
            break
        except: # 5번 이상 오류가 발견되면 중단
            if err_cnt > 5:
                print('error - id : ', data[0])
                break
            err_cnt += 1     