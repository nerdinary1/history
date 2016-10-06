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
            firstEmergence=0
            # sillokFirstEmergence.insert(man)
            # sillokFirstEmergence.update({"_id": man['_id']}, {"$set": {"실록최초등장": 0}})
            print("case1", man['이름'],firstEmergence)

        #살면서 실록에 기록된 관직이 한 번도 없는 경우에는 처음 실록에 등장한 날짜를 insert
        # elif "ref" not in keys:
        else:
            passyear = man['합격년도']

            records=[i for i in sillokIntegrated.find({"nameIndex":{"$in":[man['nameIndex']]}})]
            records.sort(key=lambda k: k['date'])

            for record in records:
                if int(record['date'].split('-')[0])<=int(passyear) or "인사-선발(選拔)" in record['subject']:
                    records.pop(0)
                else:
                    break


            if len(records) == 0:
                firstEmergence= 0
            else:
                firstEmergence=records[0]['date'].split('-')[0]

            print("case2", man['이름'],firstEmergence)
            #sillokFirstEmergence.insert(man)
            #sillokFirstEmergence.update({"_id": man['_id']}, {"$set": {"실록최초등장": firstEmergence}})



        # #실록에 기록된 관직이 한 번이라도 있었다면, 그 관직명으로 실록에 기록된 날짜를 insert
        # else:
        #     passyear = man['합격년도']
        #
        #     records=[i for i in sillokIntegrated.find({"nameIndex":{"$in":[man['nameIndex']]}})]
        #     records.sort(key=lambda k: k['date'])
        #
        #     for record in records:
        #         if int(record['date'].split('-')[0])<=int(passyear) or "인사-선발(選拔)" in record['subject']:
        #             records.pop(0)
        #         else:
        #             break
        #
        #
        #     if len(records) == 0:
        #         firstEmergence= 0
        #     else:
        #         firstEmergence=records[0]['date'].split('-')[0]
        #
        #     # if '윤' in str(firstEmergence['월']):
        #     #     firstEmergence=str(firstEmergence['년'])+"-"+ firstEmergence['월'].replace('윤','')+str(firstEmergence['일'])+"L1"
        #     # else:
        #     #     firstEmergence = str(firstEmergence['년']) + "-" + str(firstEmergence['월'])+"-"+str(firstEmergence['일']) + "L0"
        #     # firstEmergence=firstEmergence['년']
        #     # sillokFirstEmergence.insert(man)
        #     # sillokFirstEmergence.update({"_id":man['_id']}, {"$set":{"실록최초등장":firstEmergence}})
        #         print("case3", man['이름'],firstEmergence)



makeFirstEmergence()


