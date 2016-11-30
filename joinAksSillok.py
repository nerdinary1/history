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
sillokManIndex_copy = db.sillokManIndex
sillokManIndex=db.sillokManIndex
sillokManInfo = db.sillokManInfo
aksManIndex = db.aksManIndex

akssillokJoined = db.akssillokJoined

def howlong(func):
    def wrapper():
        before = time.time()
        func()
        after = time.time()
        print(after-before)
    return wrapper

def insertDB(aksman, foundsillokman, level):
    # print("level", str(level), " ", aksman['이름'], "trying to insert")
    aksmanID=aksman['_id']
    aksman['UCI']=str(aksmanID)
    del aksman['_id']
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
            print(e)
            pass
    aksman['_id']=aksmanID

# @howlong
# def makeakssillokJoined():
#
#     for aksman in aksManIndex.find(no_cursor_timeout=True):
#         print(aksman['이름'])
#     #level0 : 이름이 실록에 없는 경우
#         if sillokManIndex_copy.find({"이름":aksman['이름']}).count()==0:
#
#             insertDB(aksman, {"_id":""},0)
#
#
#     #level1 : 이름이 완전히 같은 사람이 한 명 있는 경우
#         elif sillokManIndex_copy.find({"이름":aksman['이름']}).count() ==1:
#
#             foundsillokman = sillokManIndex_copy.find_one({"이름": aksman['이름']})
#             insertDB(aksman,foundsillokman,1)
#
#
#
#
#
#     #level2 : 이름이 같은 사람은 여럿이지만 생년이 같은 사람은 단 한명인 경우
#         elif sillokManIndex_copy.find({"이름":aksman['이름'],"생년":{"$ne":0}, "생년":aksman['생년']}).count() ==1:
#             foundsillokman = sillokManIndex_copy.find_one({"이름": aksman['이름'], "생년": aksman['생년']})
#             insertDB(aksman,foundsillokman,2)
#
#
#
#
#
#     #level3 : 이름, 생년이 같지만(생년이 0인 경우도 포함) 졸년이 다른 경우
#         elif sillokManIndex_copy.find({"이름":aksman['이름'], "생년":aksman['생년'],"몰년":{"$ne":0}, "몰년":aksman['졸년']}).count()==1:
#             foundsillokman=sillokManIndex_copy.find_one({"이름":aksman['이름'], "생년":aksman['생년'],"몰년":{"$ne":0}, "몰년":aksman['졸년']})
#             insertDB(aksman,foundsillokman,3)
#
#
#
#
#
#
#     #level4 : 이름, 생년, 졸년이 같으면서(생년과 졸년이 0인 경우도 포함) aks의 관직 중 sillokManIndex의 관력이 포함되는 사람이 1명인 경우
#         elif sillokManIndex_copy.find({"이름":aksman['이름'], "생년":aksman['생년'], "몰년":aksman['졸년'], "career":{"$in":aksman['관직']}}).count()==1:
#             foundsillokman=sillokManIndex_copy.find_one({"이름":aksman['이름'], "생년":aksman['생년'], "몰년":aksman['졸년'], "career":{"$in":aksman['관직']}})
#             insertDB(aksman,foundsillokman,4)
#
#
#
#
#
#
#     #level5 : 이름, 생년, 졸년이 같으면서(생년이 0인 경우도 포함), 과거 합격 후 10년 내에 관직에 올랐던 기록이 있는 사람이 1명인 경우
#         elif sillokManIndex_copy.find({"이름":aksman['이름'], "생년":aksman['생년'], "몰년":aksman['졸년'],"careerYear":{"$elemMatch":{"$lte":aksman['합격년도']+20, "$gte":aksman['합격년도']}}}).count()==1:
#             foundsillokman=sillokManIndex_copy.find_one({"이름":aksman['이름'], "생년":aksman['생년'], "몰년":aksman['졸년'],"careerYear":{"$elemMatch":{"$lte":aksman['합격년도']+20, "$gte":aksman['합격년도']}}})
#             insertDB(aksman,foundsillokman,5)
#
#
#
#
#
#
#
#
#     #level6 : 이름이 같은 인물이 여럿이지만, 나머지 인물들은 전혀 이름 외에 기록이 없는 경우
#         elif len([i for i in sillokManIndex_copy.find({"이름": aksman['이름']}) if len(i.keys())>5]) == 1:
#             foundsillokman= [i for i in sillokManIndex_copy.find({"이름": aksman['이름']}) if len(i.keys())>5].pop()
#             insertDB(aksman,foundsillokman,6)
#
#
#
#
#         else:
#     #level7 : 분류 불가한 인물, 수작업 필요
#             print("level", str(7), " ", aksman['이름'], "not saved")
#             #insertDB(aksman,{"_id":""},7)
#
# #2016-10-08메모 동명이인인데 이 필터에 통과 못한 사람들은 분류 불가로 들어온다. 이 사람들이 들어 올 수 있도록 장치를 마련해야한다.
#
# def againakssillokJoined():
#     print("again")
#     missing = aksManIndex.find()
#     for aksman in missing:
#         print(aksman)
#         # level8 : 동명이인인데 나머지 한명은 이미 확인되어 있는 사람
#         if sillokManIndex_copy.find({"이름": aksman['이름']}).count() == 1 and akssillokJoined.find(
#             {"이름": aksman['이름']}).count() == 1:
#             foundsillokman = [i for i in sillokManIndex_copy.find({"이름": aksman['이름']}) if
#                           i['_id'] != akssillokJoined.find({'이름': aksman['이름']})].pop()
#             print(foundsillokman)
#             try:
#                 insertDB(aksman, foundsillokman, 8)
#             except:
#                 pass
#
# def treatmissing():
#     driver=webdriver.Chrome(executable_path="C:\\Users\\DH CHOI\\chromedriver")
#     for aksman in akssillokJoined.find({"level":0}):
#         print(aksman['이름'])
#         for i in sillokManIndex_copy.find({"이름":aksman['이름']}):
#             driver.get(i["_id"])
#
#         sillok_url=input("sillok url? ")
#         foundsillokman= db.sillokManIndex_copy.find_one({"_id":sillok_url})
#         recordKeys = [i for i in foundsillokman.keys()]
#         recordDict = dict()
#         for recordKey in recordKeys:
#             recordDict[recordKey] = foundsillokman[recordKey]
#         # foundsillokman의 id를 url로 넣는다.
#         url = recordDict.pop('_id')
#         recordDict['url'] = url
#         recordKeys.append('url')
#         # level을 부여
#         recordDict['level'] = 9
#         recordKeys.append('level')
#         for recordKey in recordKeys:
#             try:
#                 akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
#             except Exception as e:
#                 print(e)
#                 pass
#
#
#
#
# try:
#     for i in sillokManIndex.find():
#         sillokManIndex_copy.insert(i)
#
# except:
#     pass
#
# try:
#     # makeakssillokJoined()
#     againakssillokJoined()
# except Exception as e :
#     print(e)
#     print("main")
#     # sillokManIndex_copy.drop()
#     # akssillokJoined.drop()
# # againakssillokJoined()
# # mergesillokManIndex()
#
#
#
#
#
#
# # db = client.research
# # sillokManndex = db.sillokManIndex
# # sillokManInfo =db.sillokManInfo
# # aksManIndex = db.aksManIndex
# # aksManInfo=db.aksManInfo
# # sillokManIndex.update_many({"생년":{"$exists":0}},{"$set":{"생년":0}})
# # sillokManInfo.update_many({"생년":{"$exists":0}},{"$set":{"생년":0}})
# # sillokManIndex.update_many({"ref":{"$exists":0}},{"$set":{"ref":[]}})
# # sillokManInfo.update_many({"왕대":{"$exists":0}},{"$set":{"왕대":""}})
# # aksManIndex.update_many({"생년":""},{"$set":{"생년":0}})
# # aksManInfo.update_many({"생년":""},{"$set":{"생년":0}})
# # sillokManIndex.update_many({"_id":{"$exists":1}}, {"$set":{"동명이인":0}})

@howlong
def naiveJoin():
    sillokmans=[i for i in sillokManIndex.find()]
    for aksman in aksManIndex.find():
        for sillokman in sillokmans:
            try:
                if sillokman['한자명'] in aksman['hanalias']:
                    insertDB(aksman,sillokman,0)
            except Exception as e:
                print(e)

#생년, birth 둘 중에 하나는 0이 아닌 값이 있으면서 한명만 있는 경우
@howlong
def filter1():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        for person in persons:
            if (person['birth'] !=0 or person['생년']!=0) and len(persons) ==1:
                akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":1}})

    print("updated ",akssillokJoined.find({"level":1}).count(),"values")


#이름이 같은 사람이 여러 명일 경우, 양쪽 데이터에서 생년이 같은 사람이 1명일 경우(10년의 interval을 둠)
@howlong
def filter2():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if person['birth'] <= person['생년']+5 and person['birth']>=person['생년']-5 and person['birth'] !=0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":2}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":2}).count(),"values")

#몰년이 같은 사람이 1명인 경우
@howlong
def filter3():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if person['졸년'] == person['몰년'] and person['몰년'] !=0 and person['졸년']!=0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":3}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":3}).count(),"values")

@howlong
def filter4():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if len(set(person['career']).intersection(set(person['관직'])))>0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":4}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":4}).count(),"values")

@howlong
def filter5():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if len([i for i in person['careerYear'] if person['합격년도']<i and person['합격년도']+20<i]) >0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":5}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":5}).count(),"values")
@howlong
def filter6():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if len(person['careerYear']) > 0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":6}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":6}).count(),"values")
def filter6():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if len(person['careerYear']) > 0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":6}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":6}).count(),"values")





def filter7():
    UCIs=set(i['UCI'] for i in akssillokJoined.find({"level":0}))
    for UCI in UCIs:
        persons = [i for i in akssillokJoined.find({"UCI":UCI})]
        proper=[]
        for person in persons:
            if len(person['careerYear']) > 0:
                proper.append(person)
        if len(proper) == 1:
            akssillokJoined.update_one({"_id":persons[0]['_id']},{"$set":{"level":6}})
            persons.remove(proper.pop())
            for person in persons:
                akssillokJoined.delete_one({'_id':person['_id']})
    print("updated ",akssillokJoined.find({"level":6}).count(),"values")
naiveJoin()
filter1()
filter2()
filter3()
filter4()
filter5()
filter6()
filter6()
# naiveJoin()


