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

def makeFirstEmergence():
    db=client.research
    sdb=client.sillok
    akssillokJoined=db.akssillokJoined
    sillokIntegrated=sdb.sillokIntegrated
    sillokManInfo=db.sillokManInfo
    sillokFirstEmergence=db.sillokFirstEmergence

    for man in akssillokJoined.find(no_cursor_timeout=True):
        #아예 실록에 나오지 않는 경우
        keys=list(man.keys())

        if "url" not in keys:
            sillokFirstEmergence.insert(man)
            sillokFirstEmergence.update({"_id": man['_id']}, {"$set": {"실록최초등장": 0}})

        #살면서 실록에 기록된 관직이 한 번도 없는 경우에는 처음 실록에 등장한 날짜를 insert
        elif "ref" not in keys:
        # else:
            passyear = man['합격년도']

            records=[i['date'] for i in sillokIntegrated.find({"nameIndex":{"$in":[man['nameIndex']]}})]
            records.sort()
            for record in records:
                if int(record.split('-')[0])<int(passyear):
                    temp=records.pop()
            try:
                firstEmergence=records[0].split('-')[0]

            except:
                firstEmergence=temp.split('-')[0]
            sillokFirstEmergence.insert(man)
            sillokFirstEmergence.update({"_id": man['_id']}, {"$set": {"실록최초등장": firstEmergence}})



        #실록에 기록된 관직이 한 번이라도 있었다면, 그 관직명으로 실록에 기록된 날짜를 insert
        else:
            passyear= man['합격년도']
            idx=0
            # while True:
            #     try:
            #         t=man['ref'][idx]
            #         if sillokManInfo.find_one({"_id":t})['년']>=passyear:
            #             break
            #         idx+=1
            #     except:
            #         idx=0
            #         break
            #
            # firstId=man['ref'][idx]
            # firstEmergence=[i for i in sillokManInfo.find({"_id":firstId})].pop()


            records = [i['date'] for i in sillokIntegrated.find({"nameIndex": {"$in": [man['nameIndex']]}})]
            records.sort()

            for record in records:

                if int(record.split('-')[0]) <= int(passyear):
                    temp = records.pop(0)


            try:
                firstEmergence = records[0].split('-')[0]


            except:
                firstEmergence = temp.split('-')[0]

            # if '윤' in str(firstEmergence['월']):
            #     firstEmergence=str(firstEmergence['년'])+"-"+ firstEmergence['월'].replace('윤','')+str(firstEmergence['일'])+"L1"
            # else:
            #     firstEmergence = str(firstEmergence['년']) + "-" + str(firstEmergence['월'])+"-"+str(firstEmergence['일']) + "L0"
            # firstEmergence=firstEmergence['년']
            sillokFirstEmergence.insert(man)
            sillokFirstEmergence.update({"_id":man['_id']}, {"$set":{"실록최초등장":firstEmergence}})



makeFirstEmergence()


