#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time
import xlrd
import pandas as pd
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import TimeoutException
import telegram
import pyautogui
from random import *

# 경로바꿔주기
driver = webdriver.Chrome("C:\\Users\\LG\\Desktop\\facedetection\\chromedriver.exe")

# school_food = 학식
# weather = 날씨(네이버크롤링)
# school_information = 학사정보
# realtime_information = 실시간검색어
# library = 도서관
# school_information = 학사공지

# 막차는 생략
# 막차 = 'https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%B6%A9%EB%AC%B4%EB%A1%9C%EC%97%AD+%EB%A7%89%EC%B0%A8'


# In[2]:


def school_e_information():
    school_information=[]

    driver.get('https://engineer.dongguk.edu/bbs/board.php?bo_table=en6_1')
    date1= '/html/body/div/div[4]/div[1]/div[3]/div[2]/table/tbody/tr/td/form/table/tbody/tr[1]/td[5]/span'
    date2= '/html/body/div/div[4]/div[1]/div[3]/div[2]/table/tbody/tr/td/form/table/tbody/tr[3]/td[5]/span' 
    title1 = '/html/body/div/div[4]/div[1]/div[3]/div[2]/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/nobr/a'
    title2 = '/html/body/div/div[4]/div[1]/div[3]/div[2]/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/nobr/a'
    title = [title1, title2]
    title_into = '/html/body/div/div[4]/div[1]/div[3]/div[2]/table/tbody/tr/td/div[2]/table/tbody/tr/td[1]/div'


    f_vc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,date1))).text
    s_vc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,date2))).text

    now = datetime.now()
    
    if now.day == int(f_vc.split('-')[1]) & now.day == int(s_vc.split('-')[1]) :
        num = randint(0,1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,title[num]))).click()
        return school_information.append(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,title_into))).text), "school_e_information"
        
    elif now.day == int(f_vc.split('-')[1]) :
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,title1))).click()
        return school_information.append(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,title_into))).text), "school_e_information"

    else :
        return print("공대 공지 없음")


# In[3]:


def school_d_information():
    # 공대사이트 조사 -> 있으면 학사공지배열에 1개추가 
    
    school_e_information()
    driver.get('http://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3638&id=kr_010801000000')
    
    title = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/form[1]/table/tbody/tr[{}]/td[2]/a'
    title_into = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/table[1]/thead/tr/th'
    
    while True:
        try :      
            a=[]     
            for i in range(3):
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,title.format(randint(1,25))))).click()              
                a.append(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,title_into))).text)
                
                driver.back()
                
            a.append("school_d_information")    
            return a    
        except :
            pass      
        driver.get('http://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3638&id=kr_010801000000')

  
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,title.format(randint(1,25))))).click()
#     result = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,title_into))).text
    
#     return result

#clear


# In[30]:


def library():
    driver.get('https://lib.dongguk.edu/')
    위치 = '/html/body/div[1]/app-root/index/div[2]/app-seat/div[2]/table/tbody/tr[{}]/td[1]/span'
    이용률 = '/html/body/div[1]/app-root/index/div[2]/app-seat/div[2]/table/tbody/tr[{}]/td[6]/div/div/div[2]'
    name = '/html/body/div[2]/div[3]/div[3]/div[1]/div[3]/ul/li[{}]/h3' # iczone
    total_seat = '/html/body/div[2]/div[3]/div[3]/div[1]/div[3]/ul/li[{}]/p/span[2]' # 총 x석중
    avail_seat = '/html/body/div[2]/div[3]/div[3]/div[1]/div[3]/ul/li[{}]/p/span[1]' # 석 이용가능 
# /html/body/div[2]/div[3]/div[3]/div[1]/div[3]/ul/li[1]/h3
#     a={}
    b=[]
    for i in range(1,8,1):
        time.sleep(2)
        b.append([WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,name.format(i)))).text, WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,avail_seat.format(i)))).text])
#         a[WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,name.format(i)))).text] = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,avail_seat.format(i)))).text

    b.append("library")
    c = b[0:3], b[3:5], b[5:-1], b[-1]
    return c
    
#     return a.items() , "library"

#     return tuple(a.items())

# clear


# In[5]:


def school_food():
    
    driver.get('https://dgucoop.dongguk.edu:44649/store/store.php?w=4&l=1')
    
    남산학사식당조식경로 = '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table[3]/tbody/tr[1]/td[2]/table/tbody/tr[1]/td'
    남산학사A코너중식경로= '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table[3]/tbody/tr[3]/td[2]/table/tbody/tr[1]/td'
    남산학사A코너석식경로= '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table[3]/tbody/tr[3]/td[2]/table/tbody/tr[1]/td'
    남산학사B코너중식경로= '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table[3]/tbody/tr[3]/td[3]/table/tbody/tr[1]/td'
    d=[]
    try :
        
        a = {'남산학사식당조식' : WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,남산학사식당조식경로))).text
             ,'남산학사A코너중식' : WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,남산학사A코너중식경로))).text
             ,'남산학사A코너석식' : WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,남산학사A코너석식경로))).text
             ,'남산학사B코너중식' : WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,남산학사B코너중식경로))).text}

        now = datetime.now()
    
        if now.hour < 10 :
            
            for i in range(3):
            
                b = result[list(a.keys())[0]] = list(a.values())[0].replace('\n',' ')
                
                d.append(b)

            d.append("school_food")
            
            return d

        elif now.hour < 17 :
            
            for i in range(3):
                
                t = randint(1,3)
            
                b = result[list(a.keys())[t]] = list(a.values())[t].replace('\n',' ')
                
                d.append(b)

            d.append("school_food")
            
            return d

        elif now.hour < 20 :
            
            for i in range(3):
            
                b = result[list(a.keys())[2]] = list(a.values())[2].replace('\n',' ')
                
                d.append(b)

            d.append("school_food")
            
            return d

        else :

            for i in range(3):
                
                t = randint(0,3)
            
                b = result[list(a.keys())[t]] = list(a.values())[t].replace('\n',' ')
                
                d.append(b)

            d.append("school_food")
            
            return a
        
    except :
        
        for i in range(3):
            
            d.append("휴무")
            
        d.append("school_food")
        
        return d

#clear


# In[6]:


def weather():   
    driver.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8F%99%EA%B5%AD%EB%8C%80%ED%95%99%EA%B5%90+%EB%82%B4%EC%9D%BC%EB%82%A0%EC%94%A8&oquery=%EB%8F%99%EA%B5%AD%EB%8C%80%ED%95%99%EA%B5%90+%EB%82%A0%EC%94%A8&tqi=UOMgLlprvxsssmmCccRssssstPK-004064')   
    pat1 = '/html/body/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[4]/div[1]/div[1]'
    pat2 = '/html/body/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[4]/div[1]/div[2]'
    # 날씨
    result1 = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,pat1))).text.replace("\n도씨\n","").split('\n')
    # 미세먼지
    result2 = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,pat2))).text.replace("\n도씨\n","").split('\n')
    result3 = result1+result2  
    a=[]
    for i in range(3):
        a.append(result3)

    a.append("weather")   
    return a

# 내일날씨


# In[44]:


def realtime_information(): 
    driver.get('http://210.94.161.182/search.do')
    b=[]
    a=[]
    for i in range(1,11,1) :
        a.append(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/aside/article[1]/div/ol/li[{}]'.format(i)))).text.split('\n')[0])
    
#     tuple(a)   
    result = []   
    for i,j in enumerate(a):       
        result.append([i+1, j])
  
    b.append(result[0:3])
    b.append(result[3:6])
    b.append(result[6::])
    b.append("realtime_information")
    return b

    
#     result = list(result)


def school_s_information():
    
    driver.get('https://www.dongguk.edu/mbs/kr/jsp/academic_calender/academic_calender.jsp?academicIdx=2741&id=kr_050101000000')    
    
    now = datetime.now()
    
    if now.month == 11: 
        
        if now.day < 8 : 
            
            text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[12]/div[2]/table/tbody/tr[1]/td[2]'
            
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text))).text.replace("\n",""), "school_s_information"
    
        elif now.day < 18 : 
            
            text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[12]/div[2]/table/tbody/tr[2]/td[2]'
            
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text))).text.replace("\n",""), "school_s_information"
            
        elif now.day < 19 : 
            
            text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[12]/div[2]/table/tbody/tr[3]/td[2]'
            
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text))).text.replace("\n",""), "school_s_information"
            
        elif now.day < 21 : 
            
            text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[12]/div[2]/table/tbody/tr[4]/td[2]'
            
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text))).text.replace("\n",""), "school_s_information"
            
        elif now.day <=30 : 
            
            a=[]
            
            for i in range(3):
            
                text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[12]/div[2]/table/tbody/tr[5]/td[2]'
                
                a.append(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text))).text.replace("\n",""))

            a.append("school_d_information")
            
            return a

    elif now.month == 12:
        
        if now.day < 2:
            
            text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[13]/div[2]/table/tbody/tr[1]/td[2]'
            
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text))).text.replace("\n",""), "school_s_information"
            
        elif now.day < 4 :
            
            text = '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[13]/div[2]/table/tbody/tr[{}]/td[2]'

            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,text.randint(2,6)))).text.replace("\n",""), "school_s_information"