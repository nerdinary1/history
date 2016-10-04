
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

def countaksTosillok():
    db=client.research
    sillokManIndex=db.sillokManIndex
    aksManIndex=db.aksManIndex
    aksList=[i['이름'] for i in aksManIndex.find()]
    cnt=0
    for name in aksList:
        if sillokManIndex.find({"이름":name}).count() ==0:
            cnt+=1


def makeakssillokJoined():
    db=client.research
    sillokManIndex=db.sillokManIndex
    sillokManInfo=db.sillokManInfo
    aksManIndex=db.aksManIndex
    akssillokJoined=db.akssillokJoined
    # sillokManList=[(i['_id'],i['이름'],i['왕대'],i['생년']) for i in sillokManIndex.find()]
    #
    # for aksman in aksManIndex.find():
    #     namelist=[sillokman[1] for sillokman in sillokManList]
    #     if namelist.count(aksman['이름']) ==1:
    #         sillokmanindex=namelist.index(aksman['이름'])
    #         akssillokJoined.insert(aksman)
    #         for
    for aksman in aksManIndex.find(no_cursor_timeout=True):
    #level1 : 이름이 실록에 없는 경우
        if sillokManIndex.find({"이름":aksman['이름']}).count()==0:
            akssillokJoined.insert(aksman)
            print("level1 ",aksman['이름'])


    #level2 : 이름이 완전히 같은 사람이 한 명 있는 경우
        elif sillokManIndex.find({"이름":aksman['이름']}).count() ==1:
            akssillokJoined.insert(aksman)
            foundsillokman = [i for i in sillokManIndex.find({"이름": aksman['이름']})].pop()
            recordKeys = [i for i in foundsillokman.keys()]
            recordDict=dict()
            for recordKey in recordKeys:
                recordDict[recordKey]=foundsillokman[recordKey]
            url=recordDict.pop('_id')
            recordDict['url']=url
            recordKeys.append('url')
            for recordKey in recordKeys:
                try:
                    akssillokJoined.update({"_id":aksman["_id"]}, {"$set":{recordKey:recordDict[recordKey]}})
                except:
                    pass
            print("level2 ", aksman['이름'])





    #level3 : 이름이 같은 사람은 여럿이지만 생년이 같은 사람은 단 한명인 경우
        elif sillokManIndex.find({"이름":aksman['이름'], "생년":aksman['생년']}).count() ==1:
            akssillokJoined.insert(aksman)
            foundsillokman = [i for i in sillokManIndex.find({"이름": aksman['이름'], "생년": aksman['생년']})].pop()
            recordKeys = [i for i in foundsillokman.keys()]
            recordDict = dict()
            for recordKey in recordKeys:

                recordDict[recordKey] = foundsillokman[recordKey]
            url = recordDict.pop('_id')
            recordDict['url'] = url
            recordKeys.append('url')
            for recordKey in recordKeys:
                try:
                    akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
                except:
                    pass
            print("level3 ", aksman['이름'])







#level4 : 이름이 같고 생년이 같지만(또는 생년이 기록되어 있지 않지만(없으면 0으로 처리)), 과거 합격 후 10년 내에 관직에 올랐던 기록이 있는 사람이 1명인 경우
        elif sillokManInfo.find({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gte": aksman['생년'] + 10}}).count() >= 1 :
            ID = set(i['url'] for i in
                     sillokManInfo.find({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gt": aksman['생년'] + 10}}))
            if len(ID) == 1:
                ID=ID.pop()
                foundsillokman = [i for i in sillokManIndex.find({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gt": aksman['생년'] + 10}})].pop()
                akssillokJoined.insert(aksman)
                recordKeys = [i for i in foundsillokman.keys()]
                recordDict = dict()
                for recordKey in recordKeys:
                    recordDict[recordKey] = foundsillokman[recordKey]
                url = recordDict.pop('_id')
                recordDict['url'] = url
                recordKeys.append('url')
                for recordKey in recordKeys:
                    try:
                        akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
                    except:
                        pass
                print("level4 ", aksman['이름'])





# level5 : 이름이 같고 생년이 같지만(또는 생년이 기록되어 있지 않지만(없으면 0으로 처리)), 과거 합격 후 10~60년 내에 관직에 올랐던 기록이 있는 사람이 1명인 경우
            elif sillokManInfo.find(
                    {"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gte": aksman['생년'] + 10, "$lt":aksman['생년']+60}}).count() >= 1:
                ID = set(i['url'] for i in
                         sillokManInfo.find({"이름": aksman['이름'], '생년': aksman['생년'], "년": {"$gte": aksman['생년'] + 10, "$lt":aksman['생년']+60}}))
                if len(ID) == 1:
                    ID = ID.pop()
                    foundsillokman = [i for i in sillokManIndex.find(
                        {"이름": aksman['이름'], '생년': aksman['생년'],
                         "년": {"$gte": aksman['생년'] + 10, "$lt": aksman['생년'] + 60}})].pop()
                    akssillokJoined.insert(aksman)
                    recordKeys = [i for i in foundsillokman.keys()]
                    recordDict = dict()
                    for recordKey in recordKeys:
                        recordDict[recordKey] = foundsillokman[recordKey]
                    url = recordDict.pop('_id')
                    recordDict['url'] = url
                    recordKeys.append('url')
                    for recordKey in recordKeys:
                        try:
                            akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
                        except:
                            pass
                    print("level5 ", aksman['이름'])





#level6 : 이름이 같은 인물이 여럿이지만, 나머지 인물들은 전혀 이름 외에 기록이 없는 경우
        elif sillokManIndex.find({"이름":aksman['이름']}).count() >1:
            foundsillokman= [i for i in sillokManIndex.find({"이름": aksman['이름']}) if len(i.keys())>5]
            if len(foundsillokman) == 1:
                foundsillokman=foundsillokman.pop()

                akssillokJoined.insert(aksman)
                recordKeys = [i for i in foundsillokman.keys()]
                recordDict = dict()
                for recordKey in recordKeys:
                    recordDict[recordKey] = foundsillokman[recordKey]
                url = recordDict.pop('_id')
                recordDict['url'] = url
                recordKeys.append('url')
                for recordKey in recordKeys:
                    try:
                        akssillokJoined.update({"_id": aksman["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
                    except:
                        pass
                print("level6 ", aksman['이름'])





        else:
#분류 불가한 인물
            print("level7 ", aksman['이름'])




makeakssillokJoined()







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