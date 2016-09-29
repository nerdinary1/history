# -*- conding: utf-8 -*-
from selenium import webdriver
import random
import pymongo
import time
import re
import datetime
client = pymongo.MongoClient('143.248.156.197')

#client = pymongo.MongoClient('localhost')
URL = 'http://people.aks.ac.kr/front/tabCon/exm/exmView.aks?exmId=EXM_MN_6JOa_1439_000728&curSetPos=1&curSPos=0&isEQ=true&kristalSearchArea=P'
#driver= webdriver.Chrome(executable_path='/Users/choimarco/chromedriver')
#driver = webdriver.Chrome(executable_path="C:\Users\DH CHOI\chromedriver")
#driver.get(URL)
#item=[i.text for i in driver.find_elements_by_xpath('//div[@id="exm"]/div[4]//h5')]
#val=[i.text for i in driver.find_elements_by_xpath('//div[@class="content"]//h5')]



#paragraph지우는 함수
def deleteParagraph():
    db= client.sillok
    collectionList = db.collection_names()
    for collection in collectionList:
        print([i for i in db[collection].find({"paragraph":{"$exists":1}})])

def checkParagraph():
    db=client.sillok
    collectionList = db.collection_names()
    total =0
    for collection in collectionList:
        numArticle = len([i for i in db[collection].find({"paragraph":{"$exists":1}})])
        total+=numArticle
        print(collection,"has", numArticle, "articles")
    print(total, " articles are saved.")

#checkParagraph()
# db=client.sillok
# db['kma'].find_one_and_update({"_id":"http://sillok.history.go.kr/id/kma_10505030_002"},{"$set":{"paragraph":a}})

def countPeople():
    db=client.sillok
    collectionList=db.collection_names()
    total=0
    for collection in collectionList:
        n = 0
        for i in db[collection].find():
            n += len(i['nameIndex'])
        total+=n
        print(collection+" has "+str(n)+" nameIndex")
    print("total has"+str(total) + " name Index")

def checkPeopleCollecting():
    db=client.research
    collection = db.sillokPeople

    while True:
        first=collection.find().count()
        time.sleep(10)
        second=collection.find().count()
        print(str(datetime.datetime.now())+"collecting per 1hour "+str(second-first))

def aksPeopleCount():
    db=client.research
    collection = db.aksPeople
    print("문과 has", collection.find({"계열":"문과"}).count())
    print("무과 has", collection.find({"계열":"무과"}).count())

aksPeopleCount()