import tkinter as Tk
import tkinter.font
import multiprocessing
from queue import Empty, Full
import time
from datetime import datetime

class GuiApp(object):
   def __init__(self,q,time):
      #setting
      self.root = Tk.Tk()
      self.root.title("Test")
      self.root.geometry('1200x240')
      self.font=tkinter.font.Font(family="HY헤드라인B",size=30)

      self.text_wid1=Tk.Label(self.root,font=self.font)
      self.text_wid1.pack()
      
      self.text_wid2=Tk.Label(self.root,font=self.font)
      self.text_wid2.pack()
      #self.text_wid.pack(fill=Tk.BOTH)

      #시간 업데이트
      self.root.after(100,self.CheckQueuePoll_time())

      #큐 체크
      self.root.after(100,self.CheckQueuePoll(q,time))

      self.root.mainloop()

   def CheckQueuePoll_time(self):
      try:
         now=datetime.now()
         self.text_wid1.configure(text="{}.{}.{} {}시{}분{}초".format(str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second)))
      except Empty:
         pass
      finally:
          #1초에 한번씩 
         self.root.after(1000, self.CheckQueuePoll_time)

   def CheckQueuePoll(self,c_queue,t_queue):
      try:
         str = c_queue.get()
         time = t_queue.get()

         print("str",str)
         print("time",time)
      
         self.text_wid2.configure(text=str)
      except:
         time=100
      finally:
         self.root.after(time, self.CheckQueuePoll,c_queue,t_queue)

#데이터 생성해서 큐에 넣음
"""def GenerateData(q,time):
   for i in range(1,10):
      print ("%s초출력 테스트 생성" %(i))

      q.put("\n%s초출력" %(i))
      time.put("%s" %(i*1000))"""