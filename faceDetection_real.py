import cv2
import multiprocessing
import time
import datetime
import learning

""" 한 시간당 5번의 사이클
    하루에 3시간    이라고 가정"""

def faceDetect(q1, q2, q3, q4) :    #3초마다 화면의 얼굴을 detection하는 역할
    #실행하려면 아래 경로 수정해야 함
    detector = cv2.CascadeClassifier('C:\\Users\\LG\\Desktop\\facedetection\\opencv-master\\haarcascade_frontalface_default.xml')
    content = {}    #한 사이클에 포함된 정보의 카테고리와 송출될 때 인식된 사람의 최대 수 저장
    makeD = learning.learning()     #학습 돌리는 클래스 가져옴

    numCycle = 0    #사이클 몇 번 돌지 저장
    numCycle_in = []    #한 사이클 안에 어떤 정보가 송출되는지 목록 저장
    cycleNow = 1    #현재 몇 번째 사이클을 돌고 있는지 저장
    checkN = 0    #현재 몇 번째 정보를 송출했는지 저장
    timeP = datetime.datetime.now()     #하루 단위로 학습돌리기 위해 시간 저장

    while True :
        if timeP.strftime('%D') != datetime.datetime.now().strftime('%D') :     #하루가 지나면 학습 돌림
            data = makeD.data
            p1 = multiprocessing.Process(target=makeD.predict, args=(data,q4, ))
            p1.start()
            cycleNow = 1        #처음부터 다시 사이클을 돌기 위해 초기화
            numCycle = 0
            numCycle_in = []
            for k in makeD.data.keys() :
                makeD.data[k] = []
            timeP = datetime.datetime.now()

        if q3.qsize() :     #한 사이클이 들어옴
            numCycle_in.append(q3.get())    #사이클에 몇 개의 정보가 들어있는지 저장
            numCycle += 1

        if q1.qsize() and q2.qsize() :     #큐에 frame이 들어오면 detection 수행
            name = q2.get()             #송출되고 있는 정보의 정보 저장
            if not (name in content) :
                content[name] = 0
                
            frame = q1.get()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #흑백만 사용 가능하므로 흑백으로 변환
            gray = cv2.equalizeHist(gray)   #정확도 높이기 위해 사용(색의 양극화를 줄임)
            faces = detector.detectMultiScale(gray, 1.3, 5)    #얼굴 찾아냄

            for k in content.keys() :       #최대 얼굴 수 저장
                if name == k and content[name] < len(faces) :
                    content[name] = len(faces)

            s = datetime.datetime.now().strftime('%S')  #감지되고 있는 얼굴 단위시간마다 출력
            print(s+"\t"+str(len(faces))+"명\n")

            checkN += 1

        if (len(numCycle_in) == cycleNow) and numCycle_in[cycleNow-1] == checkN :      #한 사이클 다 돌았으면 학습 돌리기 전에 사이클 단위로 저장
            makeD.makeRow(content, cycleNow)
            content.clear()     #새로운 사이클을 돌리기 위해 초기화
            checkN = 0
            if cycleNow < numCycle :       #새로운 사이클이 이미 들어와 있을 경우
                cycleNow += 1

def faceCam(q1) :   #카메라를 실시간으로 실행하는 역할
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #화면 사이즈 조절
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ret, frame = capture.read()     #0초에도 찍어야 하므로 화면 캡처 및 detection 위해 큐에 frame을 넣음
    q1.put(frame)

    timeP = datetime.datetime.now()     #현재 시간 저장

    while  True :      #카메라를 계속 실행
        ret, frame = capture.read()

        if timeP <= datetime.datetime.now() - datetime.timedelta(seconds = 3):  #단위시간 3초마다 detection 수행
            q1.put(frame)
            timeP = datetime.datetime.now()

        k = cv2.waitKey(5)      #ESC 누르면 카메라 종료
        if k== 27 :
            break

    cap.release()       #cv2 종료
    cv2.destroyAllWindows