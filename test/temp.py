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

def howlong(func):
    def wrapper():
        before = time.time()
        func()
        after = time.time()
        print(after-before)
    return wrapper

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
    sillokManIndex = db.sillokManIndex


    suscipious=[i for i in sillokManIndex.find({"ref":{"$exists":1}}) if len(i['ref'])==1]
    for i in suscipious:
        l = list(i.keys())
        if "관력" not in l:
            sillokManIndex.update({"_id":i["_id"]}, {"$set":{"ref":[]}})

def findUnrevealed():
    db=client.research
    sdb=client.sillok
    aksManInfo=db.aksManInfo
    sillokManIndex=db.sillokManIndex
    sillokManInfo=db.sillokManInfo
    sillokIntegrated=sdb.sillokIntegrated
    aksManIndex=db.aksManIndex

    for i in sillokIntegrated.find({"nameIndex":{"$exists":1}}):
        if "M_1142086" in i['nameIndex']:
            print(i)


# checkSameName()
# removeFakeREF()
# db=client.research
# sillokManInfo=db.sillokManInfo
# sillokPeople=db.sillokPeople
# maninfolist=set([i['url'] for i in sillokManInfo.find()])
# peoplelist=set([i['url'] for i in sillokPeople.find()])
# print(len(maninfolist))
# print(len(peoplelist))
db=client.research
aksManInfo=db.aksManInfo
sillokManIndex=db.sillokManIndex
aksManIndex=db.aksManIndex
sillokManInfo=db.sillokManInfo
akssillokJoined=db.akssillokJoined
# manlist = [i for i in sillokManIndex.find()]


#
# for man in manlist:
#     aliases = [i for i in sillokManIndex.find({"이름":man['이름'], "생년":man['생년'], "몰년":man["몰년"]})]
#     if len(aliases)>=2 and man['몰년']!=0:
#         for i in aliases:
#             print(i)


# print(len([i for i in sillokManIndex.find() if i['생년']!=0 and i['몰년']==0]))
# l = [i['nameIndex'] for i in sillokManInfo.find()]
# l.sort()
# for i in l:
#     print(i)
# findUnrevealed()

# print(sillokManIndex.find_one({"careerYear":{"$elemMatch":{"$gte":1400, "$lte":1410}}}))



# @howlong
# def test():
#     sum=0
#     for i in range(1,10000000):
#         sum+=i
#     print(sum)
#
# test()
@howlong
def mergeHanname():
    for i in aksManInfo.find({"한자명":{"$exists":1}}):
        name = i['이름']
        hanname=i['한자명']
        aksManInfo.update({"_id":i["_id"]}, {"$set":{"이름":name+"("+hanname+")"}, "$unset":{"한자명":""}})

k=set()
for i in aksManIndex.find():
    k.update(set(i.keys()))

for i in k:
    print(i)
