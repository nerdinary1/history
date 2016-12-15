import pymongo
import sys
import datetime
import json
#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research
sdb=client.sillok
sillokManIndex=db.sillokManIndex_new
sillokManInfo=db.sillokManInfo
sillokIntegrated=sdb.sillokIntegrated
#add reldate into sillokManInfo

def reldateInfo():
    firstday=datetime.datetime.strptime('1392-08-05','%Y-%m-%d')
    for day in sillokManInfo.find():
        try:
            targetday=datetime.datetime.strptime(day['soldate'],'%Y-%m-%d')
            delta=(targetday-firstday).days+1
            # sillokManInfo.update_one({'_id':day['_id']},{'$set':{'rdate':delta}})
            sillokManInfo.update_one({'_id':day['_id']},{'$set':{'rdate':delta}})
            print(delta)
        except:
            continue
def reldateIndex():
    firstday=datetime.datetime.strptime('1392-08-05','%Y-%m-%d')
    for days in sillokManIndex.find({"soldate":{"$exists":1}}):
        print(days['soldate'])
        if days['soldate']==[None]:
            rdates=[None]
            sillokManIndex.update_one({'_id':days['_id']},{'$set':{'rdate':rdates}})
            print(rdates)
            continue
        rdates=[]
        for day in days['soldate']:
            try:
                targetday=datetime.datetime.strptime(day,'%Y-%m-%d')
                delta=(targetday-firstday).days+1
                rdates.append(delta)

            except Exception as e:
                rdates.append(None)
                print("except")
        print(rdates)
        sillokManIndex.update_one({'_id':days['_id']},{'$set':{'rdate':rdates}})

reldateIndex()