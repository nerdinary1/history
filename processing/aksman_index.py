import pymongo
import sys
import time
import re
#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research

aksManIndex=db.aksManIndex
aksManInfo=db.aksManInfo
collection = db.sillokManInfo
sillokManIndex=db.sillokManIndex
sillokManInfo = db.sillokManInfo
akssillokJoined = db.akssillokJoined

def nameProcessing():
    arefkey=set(["이름","초명",'일명','개명','초명2','구명','개명2'])
    for i in aksManIndex.find():
        mankey=set(i.keys())
        targets=arefkey.intersection(mankey)
        alias = []
        hanalias = []
        for target in targets:

            name = i[target]
            print(name)
            newname=re.sub(r'\([^)]*\)','',name)
            alias.append(newname)
            try:
                hanname=re.findall(r'\([^)]*\)',name)[0].strip("()")
                hanalias.append(hanname)
            except:
                pass
        aksManIndex.update({"_id":i['_id']},{"$set":{"alias":alias, "hanalias":hanalias}})
        for target in targets:
            aksManIndex.update({"_id":i['_id']},{"$unset":{target:""}})



def makeaksManIndex():

    for i in aksManInfo.find():
        try:
            originId=i.pop('_id')
            i['_id']=i['UCI']
            del i['UCI']
            aksManIndex.insert(i)
        except Exception as e:
            print(e)
            print(i)
            aksManIndex.update(
                {"_id":i["_id"]},
                {"$push":{"dup":originId}}
            )
    nameProcessing()
    aksManIndex.update_many({"관직":{"$exists":0}}, {"$set":{"관직":[]}})


makeaksManIndex()
# nameProcessing()