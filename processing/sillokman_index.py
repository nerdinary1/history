import pymongo
import sys
import time
#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research

sillokManIndex=db.sillokManIndex_new
sillokManInfo = db.sillokManInfo
akssillokJoined = db.akssillokJoined


def merge(master, slave, refpush=0):

    recordKeys = [i for i in slave.keys()]
    recordDict = dict()
    for recordKey in recordKeys:
        recordDict[recordKey] = slave[recordKey]
    #foundsillokman의 id를 url로 넣는다.
    if refpush:
        sillokManIndex.update({"_id": master["_id"]}, {"$push": {"ref": {"$each":slave['ref']}}})
        recordKeys.remove('ref')
    for recordKey in recordKeys:
        try:
            sillokManIndex.update({"_id": master["_id"]}, {"$set": {recordKey: recordDict[recordKey]}})
        except:
            pass
    sillokManIndex.delete_one({"_id":slave["_id"]})


def mergesillokManIndex():
    manlist = [i for i in sillokManIndex.find()]
    for man in manlist:
        aliases = [i for i in sillokManIndex.find({"이름":man['이름'], "생년":man['생년']})]
        if len(aliases)==2:
            first = aliases[0]
            second = aliases[1]
            #둘 다 관직에 오른 기록에 없는 경우, 첫번째 사람으로 merge
            if len(first['ref']) ==0 and len(second['ref']) == 0:
                merge(first, second)
            #둘 중 한 명만 관직에 오른 기록이 있는 경우, 그 사람으로 merge
            elif len(first['ref']) >=1 and len(second['ref']) == 0:
                merge(first, second)
            elif len(first['ref']) ==0 and len(second['ref']) >= 1:
                merge(second, first)
            #둘 다 기록이 있는 경우, 동명이인임을 표시한다
            else:
                d = set(['왕대','왕력','년','월','일','관력','형태','_id','ref','동명이인','몰년','nameIndex'])
                if first['생년'] == 0 and second['생년'] ==0:
                    d.add("생년")
                first_keys=set(first.keys()).difference(d)
                second_keys=set(second.keys()).difference(d)


                if first_keys==second_keys and first_keys != set(["이름","본관", "성씨"]) and second_keys!=set(["이름","본관","성씨"]):

                    cnt = 0
                    for first_key in first_keys:
                        try:
                            if first[first_key] == second[first_key]:
                                cnt+=1
                        except:
                            pass
                    print(first_keys)
                    print(len(first_keys), cnt)

                    if len(first_keys) == cnt:
                        print("merge")
                        merge(first,second,1)





                print(first['_id'],second['_id'])
    exceptional = [i for i in sillokManIndex.find({"이름":"윤의립(尹義立)"})]
    merge(exceptional[0],exceptional[1])
    exceptional = [i for i in sillokManIndex.find({"이름":"윤저(尹柢)"})]
    merge(exceptional[0],exceptional[1])
    exceptional = [i for i in sillokManIndex.find({"이름":"조영무(趙英茂)"})]
    merge(exceptional[0],exceptional[1])

def removeFakeREF():
    db = client.research
    sillokManInfo = db.sillokManInfo
    sillokManIndex = db.akssillokJoined
    akssillokJoined = db.akssillokJoined
    suscipious=[i for i in sillokManIndex.find({"ref":{"$exists":1}}) if len(i['ref'])==1]
    for i in suscipious:
        l = list(i.keys())
        if "형" not in l:
            sillokManIndex.update({"_id":i["_id"]}, {"$unset":{"ref":1}})

def makeNameIndex():
    db=client.research
    sillokManInfo=db.sillokManInfo
    sillokManIndex=db.sillokManIndex
    akssillokJoined=db.akssillokJoined
    nameList= [i["_id"] for i in sillokManIndex.find()]
    for url in nameList:
        sillokManIndex.update_many({"_id":url}, {"$set":{"nameIndex":url[-9::]}})
    for man in db.sillokManInfo.find():
        sillokManInfo.update_many({"url": man['url']}, {"$set": {"nameIndex": man['url'][-9::]}})
        # akssillokJoined.update_many({"_id": url}, {"$set": {"nameIndex": url[-9::]}})


def addCareerGroup():

    manlist = [i for i in sillokManIndex.find()]

    for man in manlist:
        print(man)
        careers = set()
        career_year= set()
        refs = [i for i in man['ref']]
        for ID in refs:
            careers.add(sillokManInfo.find_one({"_id":ID})['관력'])
            career_year.add(sillokManInfo.find_one({"_id":ID})['년'])
        sillokManIndex.update({"_id":man['_id']},{"$set":{"career":list(careers), "careerYear":sorted(list(career_year))}})



def makeIndex():
    for record in sillokManInfo.find():

        url = record.pop('url')
        originId=record.pop('_id')
        recordKeys=list(record.keys())
        recordDict=dict()

        for recordKey in recordKeys:
            recordDict[recordKey] = record[recordKey]
            recordDict["_id"] = url
            recordDict["ref"] = [originId]
        try:
            sillokManIndex.insert(recordDict)
        except :
            sillokManIndex.update({"_id":url}, {"$push":{"ref":originId}})

    sillokManIndex.update_many({"생년":{"$exists":0}},{"$set":{"생년":0}})
    sillokManIndex.update_many({"몰년":{"$exists":0}},{"$set":{"몰년":int(0)}})
    sillokManIndex.update_many({"본관":{"$exists":0}},{"$set":{"본관":""}})

    removeFakeREF()
    sillokManIndex.delete_many({"이름":""})

    exceptional = [i for i in sillokManIndex.find({"이름":"조영무(趙英茂)"})]
    merge(exceptional[0],exceptional[1])

    sillokManIndex.delete_many({"이름":""})
    spaceman=[i for i in sillokManIndex.find() if " " in i['이름']]
    for i in spaceman:
        newname=i['이름'].replace(' ','')
        sillokManIndex.update({"_id":i['_id']},{"이름":newname})
    addCareerGroup()



makeIndex()
