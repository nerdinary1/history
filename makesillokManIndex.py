import pymongo
import sys
#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research
collection = db.sillokManInfo
sillokManIndex=db.sillokManIndex
sillokManInfo = db.sillokManInfo
akssillokJoined = db.akssillokJoined

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

def makeNullKey():
    for i in sillokManIndex.find():

        keys = list(i.keys())

        if "생년" not in keys:
            sillokManIndex.update({"_id":i["_id"]},{"$set":{"생년":""}})
        if "본관" not in keys:
            sillokManIndex.update({"_id":i["_id"]},{"$set":{"본관":""}})

for record in collection.find():
    try:
        url = record.pop('url')
        originId=record.pop('_id')
        recordKeys=list(record.keys())
        recordDict=dict()
        if "생년" not in recordKeys:
            recordDict['생년'] = ''
            recordKeys.append('생년')
        if '본관' not in recordKeys:
            recordDict['본관'] = ''
            recordKeys.append('본관')
        for recordKey in recordKeys:
            recordDict[recordKey] = record[recordKey]
            recordDict["_id"] = url
            recordDict["ref"] = [originId]
        sillokManIndex.insert(recordDict)
    except :
        sillokManIndex.update({"_id":url}, {"$push":{"ref":originId}})
