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
    collection = db.sillokManInfo

    while True:
        first=collection.find().count()
        time.sleep(10)
        second=collection.find().count()
        print(str(datetime.datetime.now())+"collecting per 1hour "+str(second-first))

def aksManInfoCount():
    db=client.research
    collection = db.aksManInfo
    print("문과 has", collection.find({"계열":"문과"}).count())
    print("무과 has", collection.find({"계열":"무과"}).count())

def missingsillokManInfo():
    db=client.research
    sillokManURLUnique = db.sillokManURLUnique
    sillokManInfo=db.sillokManInfo
    nameList = [i['_id'] for i in sillokManURLUnique.find()]
    infoList = list(set([i['url'] for i in sillokManInfo.find()]))
    uncrawled=[]
    for name in nameList:
        if name not in infoList:
            print(name)
            uncrawled.append(name)
    print(len(uncrawled))

def treatAnonymousaks():
    db=client.research
    aksManInfo=db.aksManInfo
    anonymous=[i['_id'] for i in aksManInfo.find({"UCI":{"$exists":0}})]
    print(anonymous)
    for i in anonymous:
        num=str(anonymous.index(i)+1)
        aksManInfo.update_one({"_id":i},{"$set":{"UCI":"anonymous"+num}})

def showSameName():
    db=client.research
    aksManInfo=db.aksManInfo
    l = [(i['이름'],i['합격년도']) for i in aksManInfo.find()]
    UCI=set(i['UCI'] for i in aksManInfo.find())
    print(len(l))
    print(len(UCI))
    s=set(l)
    s=list(s)
    print(len(s))
    for i in l:
        if l.count(i) !=1:
            print(i)
def makeaksManIndex():
    db=client.research
    aksManIndex=db.aksManIndex
    aksManInfo=db.aksManInfo
    for i in aksManInfo.find():
        try:
            originId=i.pop('_id')
            print(i)
            i['_id']=i['UCI']
            del i['UCI']
            aksManIndex.insert(i)
        except:
            print("ss")
            aksManIndex.update(
                {"_id":i["_id"]},
                {"$push":{"dup":originId}}
            )


def checkSameName():
    db=client.research
    aksManIndex=db.aksManIndex

    namekingList=[(i['이름'],i['생년']) for i in aksManIndex.find()]
    fullList=[i for i in aksManIndex.find()]

    for i in fullList:
        if namekingList.count((i['이름'],i['생년'])) >1 and i['이름'] !="■■■(■■■)":
            print(namekingList.count((i['이름'],i['생년'])),"   ",i['이름'])

def checkaksTosillok():
    db = client.research
    aksManIndex = db.aksManIndex
    sillokManInfo=db.sillokManInfo

def countsillokManInfo():
    db=client.research
    sillokManInfo = db.sillokManInfo
    sillokManIndex=db.sillokManIndex
    infolist=[i['url'] for i in sillokManInfo.find()]
    indexlist=[i['_id'] for i in sillokManIndex.find()]
    for i in indexlist:
        if i not in infolist:
            print(i)
def makeNameIndex():
    db=client.research
    sillokManInfo=db.sillokManInfo
    sillokManIndex=db.sillokManIndex
    akssillokJoined=db.akssillokJoined
    nameList= [i["_id"] for i in sillokManIndex.find()]
    for url in nameList:
        sillokManIndex.update_many({"_id":url}, {"$set":{"nameIndex":url[-9::]}})
        sillokManInfo.update_many({"url": url}, {"$set": {"nameIndex": url[-9::]}})
        akssillokJoined.update_many({"_id": url}, {"$set": {"nameIndex": url[-9::]}})

def removeFakeREF():
    db = client.research
    sillokManInfo = db.sillokManInfo
    sillokManIndex = db.akssillokJoined
    akssillokJoined = db.akssillokJoined
    suscipious=[i for i in sillokManIndex.find({"ref":{"$exists":1}}) if len(i['ref'])==1]
    for i in suscipious:
        l = list(i.keys())
        if "관력" not in l:
            sillokManIndex.update({"_id":i["_id"]}, {"$unset":{"ref":1}})


# checkSameName()
removeFakeREF()
# db=client.research
# sillokManInfo=db.sillokManInfo
# sillokPeople=db.sillokPeople
# maninfolist=set([i['url'] for i in sillokManInfo.find()])
# peoplelist=set([i['url'] for i in sillokPeople.find()])
# print(len(maninfolist))
# print(len(peoplelist))
