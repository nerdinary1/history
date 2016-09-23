from selenium import webdriver
import random
import pymongo
import time
import re
#client = pymongo.MongoClient('localhost')
URL = 'http://people.aks.ac.kr/front/tabCon/exm/exmView.aks?exmId=EXM_MN_6JOa_1439_000728&curSetPos=1&curSPos=0&isEQ=true&kristalSearchArea=P'
driver= webdriver.Chrome(executable_path='/Users/choimarco/chromedriver')
#driver = webdriver.Chrome(executable_path="C:\Users\DH CHOI\chromedriver")
driver.get(URL)
item=[i.text for i in driver.find_elements_by_xpath('//div[@id="exm"]/div[4]//h5')]
val=[i.text for i in driver.find_elements_by_xpath('//div[@class="content"]//h5')]

for i in item:
    print(i)
driver.close()
# for i in examInfo:
#     print(i.text)