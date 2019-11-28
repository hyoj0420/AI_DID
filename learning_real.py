import numpy as np
import os
from collections import defaultdict

class learning:
    data = defaultdict      #지금까지 송출되고 있는 정보 목록 저장
    data = {}
    path = "C:\\Users\\LG\\Desktop\\facedetection\\"       #데이터 저장하기 위한 경로

    def __init__(self) :
        pass

    def makesit(self, dataSet, category, start, finish, q4) :
            m, n = dataSet.shape
            A = np.array([dataSet[:,0], np.ones(m)]).T
            b = dataSet[:, 1]
            Q, R = self.qr_householder(A)
            b_hat = Q.T.dot(b)

            R_upper = R[:n, :]
            b_upper = b_hat[:n]

            x = np.linalg.solve(R_upper, b_upper)       #데이터를 기준으로 그래프 기울기를 구함
            slope, intercept = x        #a=slope, b=intercept

            print("\n"+category)
            for i in range(start, finish) :
                q4.put({'대분류' : k , '시간단위' : i+1, '사람수예측': slope*(i+1)+intercept})
            return

    """실제 데이터들과 예측값 사이의 오차가 최소한이 되는 그래프를 찾기 위한 과정
        오차 제곱의 합 차이가 최소한이 되는 그래프 찾기
        하우스홀더 변환을 사용해 Q,R을 찾아냄"""
    def qr_householder(self, dataSet) :
        m, n = dataSet.shape
        Q = np.eye(m)
        R = dataSet.copy()

        for j in range(n) :
            x = R[j:, j]
            normx = np.linalg.norm(x)
            rho = -np.sign(x[0])
            u1 = x[0]-rho*normx
            u = x/u1
            u[0] = 1
            beta = -rho * u1/normx

            R[j:, :] = R[j:, :]-beta*np.outer(u,u).dot(R[j:, :])
            Q[:, j:] = Q[:, j:]-beta*Q[:, j:].dot(np.outer(u,u))

        return Q,R      #Q는 Orthogonal Matrix, R은 Upper Triangle Matrix

    def makeRow(self, contentList, num) :   #하루 내 사이클로 데이터 적재
        for k in contentList.keys() :       #사이클 내 포함되지 않은 정보는 감지된 사람 수가 0명인 걸로 자동 저장
            if not (k in self.data) :
                a = []
                for i in range(num-1) :
                    a.append(0)
                a.append(contentList[k])
                self.data[k] = a
            else :
                self.data[k].append = contentList[k]        #사이클 내 포함된 정보는 감지된 최대 사람 수 저장
        for k in self.data.keys() :
            if len(self.data[k]) < num :
                self.data[k].append(0)

    def predict(self, data, q4) :       #적재된 데이터로 사람 수 예측
        for k in data.keys() :
            dataSet = np.array([])      #학습 돌리기 위한 데이터셋 생성
            dataList = data[k]
            turn = len(dataList)        #사이클 수 확인
            if not(turn) :      #사이클 수가 부족한 경우를 대비해 1로 둠
                turn = 1
            name = self.findData(self.path, k)      #데이터가 저장된 파일 찾기
            
            if name :       #데이터가 저장된 파일이 존재하면 데이터를 불러온다
                f = open(name, 'r')
                for line in f.readlines() :
                    arr = line.splitlines()[0].split(',')
                    dataSet = np.append(dataSet, [int(arr[0]), int(arr[1])])
                    if turn<int(arr[0]) :
                        turn = int(arr[0])          #전체 사이클 수 확인
                f.close()

            f = open(self.path+k+".txt", 'a')       #새로운 데이터를 데이터셋에 포함시키고 데이터가 저장된 파일에 추가
            for i in range(len(dataList)) :
                dataSet = np.append(dataSet, [(i // 60)+1, dataList[i]])
                if i == 0 and name :
                    f.write("\n")
                f.write(str((i // 60)+1)+","+str(dataList[i]))
                if i != len(dataList) -1 :
                    f.write("\n")
            f.close()
            dataSet_m = np.array([])
            dataSet_d = np.array([])
                
            dataSet = dataSet.reshape(-1,2)     #학습 돌리기 위한 행렬 형태로 변환
            for i in range(len(dataSet)) :
                if (dataSet[i, [0]]>2) :
                    dataSet_d = np.append(dataSet_d, dataSet[i])
                else :
                    dataSet_m = np.append(dataSet_d, dataSet[i])
            dataSet_m = dataSet_m.reshape(-1,2)
            dataSet_d = dataSet_d.reshape(-1,2)

            """y=ax+b 형태의 선형 그래프를 그림"""

            self.makesit(dataSet_m, k, 0, 12)
            self.makesit(dataSet_d, k, 12, 24)
            self.data[k]=[]     #초기화
        return

    def findData(self, path, name) :        #해당 카테고리에 대한 데이터 파일이 존재하는지 확인
        fileNames = os.listdir(path)

        for k in fileNames :
            if k == name+".txt" :
                return path+k 
        return False