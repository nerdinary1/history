#실록 기사의 음력 날짜를 양력 날짜로 바꾸는 함수

from selenium import webdriver
import random
import pymongo
import time
import sys
import re
import hanja
from kings import *
import datetime
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
    driver=webdriver.Firefox()
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')
    driver=webdriver.Chrome(executable_path="C:\Users\DH CHOI\chromedriver.exe")
db=client.sillok
sillokIntegrated=db.sillokIntegrated







#한국천문연구원 사이트를 이용하여 날짜변환
def processLunar(year, month, day, lunar = "1"):
    driver.get('http://astro.kasi.re.kr/Life/Knowledge/solar2lunar/convert_daily_l2s.php')
    driver.find_element_by_css_selector("input[name=\"lun_year\"]").send_keys(year)
    driver.find_element_by_css_selector("input[name=\"lun_month\"]").send_keys(month)
    driver.find_element_by_css_selector("input[name=\"lun_day\"]").send_keys(day)
    driver.find_element_by_css_selector("input[value=\""+"3"+"\"]").click()
    driver.find_element_by_css_selector('input[alt="변환"').click()

    date = driver.find_element_by_css_selector("table.graytable tbody tr td").text
    newyear = re.compile(r'\d{4}').search(date).group()
    newmonth = re.compile(r'\d{2}월').search(date).group().replace('월','')
    newday = re.compile(r'\d{2}일').search(date).group().replace('일','')


    return int(newyear), int(newmonth), int(newday)

#기사에서 날짜 부분을 읽어오는 함수
def readDate():
    for page in sillokIntegrated.find():
        date=page['date'].split('-')
        year=date[0]
        month=date[1]
        day=date[2].split('L')[0]
        newdate = processLunar(year, month, day)
        sillokIntegrated.update_one({"_id":page['_id']},{"$set":{"date":str(newdate[0])+"-"+str(newdate[1])+"-"+str(newdate[2])}})


readDate()


