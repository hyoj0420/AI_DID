import faceDetection as fr
import crawling as cr
import gui
import datetime
import pandas as pd
import multiprocessing
import random
from tqdm import tqdm
import pymysql

if __name__ == "__main__" :
    timeN = datetime.datetime.now()
    init = 0
    priority_data2 = []

    m = multiprocessing.Manager()
    timeQ = m.Queue()
    q5 = m.Queue() #gui
    q4 = m.Queue()
    q2 = m.Queue()
    q3 = m.Queue()
    q1 = m.Queue()          #프로세스들이 공유하는 큐 생성
    p1 = multiprocessing.Process(target=fr.faceCam, args=(q1, ))       #프로세스 1 생성
    p2 = multiprocessing.Process(target=fr.faceDetect, args=(q1, q2, q3, q4, ))    #프로세스 2 생성
    p1.start()
    p2.start()
    conn = pymysql.connect(host='localhost', user='root', password='Wjddudwns12@', db='uahan', charset='utf8')
    curs = conn.cursor()
    
    while True :
        if timeN.strftime('%D') != datetime.datetime.now().strftime('%D') :
            if init :
                # 효정 데이터 받아옴 
                # 쌓인 것을 가져오기 
                while (q4.qsize() > 0) :
                    priority_data = priority_data.append(q4.get(), ignore_index=True)
            elif not init :
                for i in range(24) :
                    for k in ['weather', 'school_food', 'school_info', 'realtime_info', 'library', 'school_s_info'] :
                        priority_data = priority_data.append({'대분류' : k, '시간단위' : i+1, '사람수예측' :1}, ignore_index=True)

            priority_data.sort_values(by='시간단위')
            # 송출시간
            ab=[]
            try : 
                for i in range(len(priority_data)):
                    ab.append(int(priority_data.iloc[i,2]/ sum(priority_data.loc[priority_data['시간단위'] == priority_data.iloc[i,1] ,['사람수예측']].사람수예측)*20)*3)
            except :     
                print("열 안맞음")    
                pass

            ab= {'송출시간' : ab}
            ab=pd.DataFrame(ab)
            priority_data2 = pd.concat([priority_data,ab], axis=1)

            # 카메라 사람 수 인식정보 받을 dataframe, 1시간 단위
            # 6은 시간단위 개수만큼 

            for i in range(24) :
                count = 60
                while(count) :
                    for k in range(i*6, (i+1)*6, 1) :
                        n = priority_data2.iloc[k,3] / 3
                        if not (k+6 // 6) :
                            q3.put(6)
                        for j in range(int(n)):
                            q2.put(priority_data2.iloc[k,0])
                    count -= 1

        if not init or timeN + datetime.timedelta(seconds=20) >= datetime.datetime.now() :
            if not init :
                t1 = multiprocessing.Process(target=gui.GuiApp,args=(q5,timeQ, ))
                t1.start()
            # 미리 크롤링 해옴
            pre1= cr.school_d_information()
            pre2 = cr.library()
            pre3 = cr.school_food()
            pre4 = cr.weather()
            pre5 = cr.realtime_information()
            pre6 = cr.school_s_information()
            # DataFrame 형태

            # 내용1
            a1=[]
            # 내용2
            a2=[]
            # 내용3
            a3=[]
            # 대분류
            b=[]
            # 송출시간
            c=[]
            # 시간단위
            d=[]

            # QUeue 형태
            # 내용
            cue_a =[]
            # 대분류
            cue_b =[]
            # 송출시간
            cue_c =[]
            # 시간단위
            cue_d =[]

            # 크롤링 데이터 매핑시키기 
            # 시간단위 개수만큼
            Y = priority_data2.loc[:, ['대분류']].values
            for i in tqdm(range(0,6,1)):    
                if Y[i,0] == 'school_food' :
                    a1.append(pre3[0])
                    a2.append(pre3[1])
                    a3.append(pre3[2])
                    b.append(pre3[-1])
                    c.append(priority_data2.iloc[i,3]/3)
                    d.append(priority_data2.iloc[i,2])
                    
                    cue_a.append(pre3[0])
                    cue_a.append(pre3[1])
                    cue_a.append(pre3[2])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    
                    
                elif Y[i,0] == 'weather' :
                    a1.append(pre4[0])
                    a2.append(pre4[1])
                    a3.append(pre4[2])
                    b.append(pre4[-1])
                    c.append(priority_data2.iloc[i,3]/3)
                    d.append(priority_data2.iloc[i,2])
                    
                    cue_a.append(pre4[0])
                    cue_a.append(pre4[1])
                    cue_a.append(pre4[2])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    
                elif Y[i,0] == 'school_info' :
                    a1.append(pre1[0])
                    a2.append(pre1[1])
                    a3.append(pre1[2])
                    b.append(pre1[-1])
                    c.append(priority_data2.iloc[i,3]/3)     
                    d.append(priority_data2.iloc[i,2])
                    
                    cue_a.append(pre1[0])
                    cue_a.append(pre1[1])
                    cue_a.append(pre1[2])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])

                elif Y[i,0] == 'school_s_info' :
                    a1.append(pre6[0])
                    a2.append(pre6[1])
                    a3.append(pre6[2])
                    b.append(pre6[-1])
                    c.append(priority_data2.iloc[i,3]/3)                
                    d.append(priority_data2.iloc[i,2])

                    cue_a.append(pre6[0])
                    cue_a.append(pre6[1])
                    cue_a.append(pre6[2])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])

                elif Y[i,0] == 'library' :
                    a1.append(pre2[0])
                    a2.append(pre2[1])
                    a3.append(pre2[2])
                    b.append(pre2[-1])
                    c.append(priority_data2.iloc[i,3]/3)         
                    d.append(priority_data2.iloc[i,2])

                    cue_a.append(pre2[0])
                    cue_a.append(pre2[1])
                    cue_a.append(pre2[2])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                            
                elif Y[i,0] == 'realtime_info' :
                    a1.append(pre5[0])
                    a2.append(pre5[1])
                    a3.append(pre5[2])
                    b.append(pre5[-1])
                    c.append(priority_data2.iloc[i,3]/3)             
                    d.append(priority_data2.iloc[i,2])
                    
                    cue_a.append(pre5[0])
                    cue_a.append(pre5[1])
                    cue_a.append(pre5[2])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_b.append(priority_data2.iloc[i,0])
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_c.append(priority_data2.iloc[i,3]/3)
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])
                    cue_d.append(priority_data2.iloc[i,2])

            # 1시간 단위 맞추기

            if sum(cue_c) < 60 :
                n = ((60-sum(cue_c))/3)
                for i in range(int(n)):
                    cue_c[random.randint(1, len(cue_c)-1)] += 3 

            # 출력부에 보내줄 데이터 

            # DataFrame

            aList= {}

            aList['내용'] = cue_a
            aList['대분류'] = cue_b
            aList['시간'] = cue_c
            aList['시간단위'] = cue_d

            temp = aList['내용']
            tempp = aList['시간']
            # Queue
            for i in range(len(temp)) :
                q5.put(temp[i])
                timeQ.put(int(tempp[i]*1000))
            
            for i in range(len(cue_a)):
                t = (str(i), str(cue_a[i]), str(cue_b[i]), str(cue_c[i]), str(cue_d[i]))
                sql = "insert into 전광판(인덱스, 내용, 대분류, 시간, 시간단위) values (%s, %s, %s, %s, %s)"
                curs.execute(sql, t)
                conn.commit()
            init += 1

        timeN = datetime.datetime.now()