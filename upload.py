#-*- coding: utf-8 -*-
from multiprocessing import cpu_count, Pool # excel 파일을 효율적으로 변수에 저장하기 위해서, 여러개의 cpu에 공동작업을 실행시켜 작업을 하게한다. 
import pandas as pd # 엑셀 파일을 읽는데 활용

from upload_db import upload_db # 모듈(함수)를 사용하는 역할을 한다.
import tqdm # cpu를 이용한 xlsx 파일 일기의 진행현황을 그래프로 표현

if __name__ == '__main__':
    df = pd.read_excel('gwanju_cctv.xlsx') # 판다스로 excel 파일을 읽음
    datas = df.values.tolist() # excel 파일의 데이터프레임을 가져와서(values) 리스트 형식으로 바꾸는 역할을 한다(tolist)

    # for data in datas:
    #     upload_db(data)
    #     break
    #print(datas)
    mt = cpu_count() # cpu의 갯수를 표시해주는 메서드를 mt로 선언 
    print("cpu >> ", mt) # cpu의 갯수를 출력

    p = Pool(mt) # mt라는 cpu의 갯수를 카운팅 해주는 함수에 결과값인 mt를 병렬구조로 실행 유닛을 만들어 cpu로 멀티프로세싱을 하기 위해 필요한 정보인 cpu 개수를 넣어준다.

    for _ in tqdm.tqdm(p.imap_unordered(upload_db, datas), total = len(datas)): # 진행 현황을 보여주기 위해 그래프를 그리는 요소인 tqdm을 이용하여, 이에 필요한 데이터들을 입력하여 콘솔창에 출력한다.
        pass                                                                    # 동시에 앞에서 선언해준 upload_db 라는 모듈을 이용하여 cpu를 이용하여 변수에 저장한 데이터를 upload_db.py 파일로 전송한다.
    p.close()
    p.join()