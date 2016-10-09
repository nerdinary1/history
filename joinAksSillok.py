from selenium import webdriver
import random
import pymongo
import time
import re
import datetime
import sys
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db = client.research
sillokManIndex = db.sillokManIndex
sillokManInfo = db.sillokManInfo
aksManIndex = db.aksManIndex
akssillokJoined = db.akssillokJoined
def countaksTosillok():
    db=client.research
    sillokManIndex=db.sillokManIndex
    aksManIndex=db.aksManIndex
    aksList=[i['이름'] for i in aksManIndex.find()]
    cnt=0
    for name in aksList:
        if sillokManIndex.find({"이름":name}).count() ==0:
            cnt+=1
def insertDB(aksman, foundsillokman, level):
    akssillokJoined.insert(aksman)
    recordKeys = [i for i in foundsillokman.keys()]
    recordDict = dict()
    for recordKey in recordKeys:
        recordDict[recordKey] = foundsillokman[recordKey]
    #foundsillokman의 id를 url로 넣는다.
    url = recordDict.pop('_id')
    recordDict['url'] = url
    recordKeys.append('url')
    #level을 부여
    recordDict['level'] = level
    recordKeys.append('level')

    for recordKey in recordKeys:
        try:
            akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
        except Exception as e:

            pass
    print("level", str(level), " ", aksman['이름'])

def makeakssillokJoined():

    for aksman in aksManIndex.find(no_cursor_timeout=True):

    #level1 : 이름이 실록에 없는 경우
        if sillokManIndex.find({"이름":aksman['이름']}).count()==0:
            insertDB(aksman, {"_id":""},1)


    #level2 : 이름이 완전히 같은 사람이 한 명 있는 경우
        elif sillokManIndex.find({"이름":aksman['이름']}).count() ==1:

            foundsillokman = sillokManIndex.find_one({"이름": aksman['이름']})
            insertDB(aksman,foundsillokman,2)





    #level3 : 이름이 같은 사람은 여럿이지만 생년이 같은 사람은 단 한명인 경우
        elif sillokManIndex.find({"이름":aksman['이름'], "생년":aksman['생년']}).count() ==1:

            foundsillokman = sillokManIndex.find_one({"이름": aksman['이름'], "생년": aksman['생년']})
            insertDB(aksman,foundsillokman,3)







#level4 : 이름이 같고 생년이 같지만(또는 생년이 기록되어 있지 않지만(없으면 0으로 처리)), 과거 합격 후 10년 내에 관직에 올랐던 기록이 있는 사람이 1명인 경우
        elif sillokManInfo.find({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$lte": aksman['합격년도'] + 10}}).count() == 1 :

            foundsillokman = sillokManIndex.find_one({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$lte": aksman['합격년도'] + 10}})
            insertDB(aksman,foundsillokman,4)





# level5 : 이름이 같고 생년이 같지만(또는 생년이 기록되어 있지 않지만(없으면 0으로 처리)), 과거 합격 후 10~60년 내에 관직에 올랐던 기록이 있는 사람이 1명인 경우
        elif sillokManInfo.find(
                {"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gte": aksman['합격년도'] + 10, "$lt":aksman['합격년도']+60}}).count() == 1:


            foundsillokman = sillokManIndex.find_one({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gte": aksman['합격년도'] + 10, "$lt":aksman['합격년도']+60}})

            insertDB(aksman,foundsillokman,5)



#level6: 이름이 같은 인물이 여럿이지만, 생년에 대한 정보는 없고 관직에 오른 기록이 10년 내에 있던 사람
        elif sillokManInfo.find({"이름":aksman['이름'], "년": {"$lte": aksman['합격년도'] + 10}}).count() ==1:
            foundsillokman= sillokManIndex.find_one({"이름":aksman['이름'], "년": {"$lte": aksman['합격년도'] + 10}})
            insertDB(aksman,foundsillokman,6)




#level7 : 이름이 같은 인물이 여럿이지만, 나머지 인물들은 전혀 이름 외에 기록이 없는 경우
        elif len([i for i in sillokManIndex.find({"이름": aksman['이름']}) if len(i.keys())>5]) == 1:
            foundsillokman= [i for i in sillokManIndex.find({"이름": aksman['이름']}) if len(i.keys())>5].pop()
            insertDB(aksman,foundsillokman,7)




        else:
#분류 불가한 인물
            print(aksman['이름'])
            insertDB(aksman,{"_id":""},0)

#2016-10-08메모 동명이인인데 이 필터에 통과 못한 사람들은 분류 불가로 들어온다. 이 사람들이 들어 올 수 있도록 장치를 마련해야한다.

def againakssillokJoined():
    missing = akssillokJoined.find({"level":0})
    for aksman in missing:
        print(aksman)
        # level8 : 동명이인인데 나머지 한명은 이미 확인되어 있는 사람
        if sillokManIndex.find({"이름": aksman['이름']}).count() == 2 and akssillokJoined.find(
            {"이름": aksman['이름']}).count() == 1:
            foundsillokman = [i for i in sillokManIndex.find({"이름": aksman['이름']}) if
                          i['_id'] != akssillokJoined.find({'이름': aksman['이름']})].pop()
            print(foundsillokman)
            try:
                insertDB(aksman, foundsillokman, 8)
            except:
                pass

def treatmissing():
    driver=webdriver.Chrome(executable_path="C:\\Users\\DH CHOI\\chromedriver")
    for aksman in akssillokJoined.find({"level":0}):
        print(aksman['이름'])
        for i in sillokManIndex.find({"이름":aksman['이름']}):
            driver.get(i["_id"])

        sillok_url=input("sillok url? ")
        foundsillokman= db.sillokManIndex.find_one({"_id":sillok_url})
        recordKeys = [i for i in foundsillokman.keys()]
        recordDict = dict()
        for recordKey in recordKeys:
            recordDict[recordKey] = foundsillokman[recordKey]
        # foundsillokman의 id를 url로 넣는다.
        url = recordDict.pop('_id')
        recordDict['url'] = url
        recordKeys.append('url')
        # level을 부여
        recordDict['level'] = 9
        recordKeys.append('level')
        for recordKey in recordKeys:
            try:
                akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
            except Exception as e:

                pass

#sillokManIndex에서 생년과 이름이 같은 사람을 merge하는 함수


#sillokManIndex에서 생년과 이름이 같으면 동일인인지 확인하는 함수
def checkMergeness():
    manlist = [i for i in sillokManIndex.find()]
    for man in manlist:

        if sillokManIndex.find({"이름":man['이름'], "생년":man['생년']}).count()==2:
            print([i['url'] for i in sillokManIndex.find({"이름":man['이름'], "생년":man['생년']})])

checkMergeness()
# makeakssillokJoined()
# againakssillokJoined()







# db = client.research
# sillokManndex = db.sillokManIndex
# sillokManInfo =db.sillokManInfo
# aksManIndex = db.aksManIndex
# aksManInfo=db.aksManInfo
# sillokManIndex.update_many({"생년":{"$exists":0}},{"$set":{"생년":0}})
# sillokManInfo.update_many({"생년":{"$exists":0}},{"$set":{"생년":0}})
# sillokManIndex.update_many({"왕대":{"$exists":0}},{"$set":{"왕대":""}})
# sillokManInfo.update_many({"왕대":{"$exists":0}},{"$set":{"왕대":""}})
# aksManIndex.update_many({"생년":""},{"$set":{"생년":0}})
# aksManInfo.update_many({"생년":""},{"$set":{"생년":0}})