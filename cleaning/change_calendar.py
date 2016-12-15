import pymongo
import sys
import time
import json
#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research
sdb=client.sillok
collection = db.sillokManInfo
sillokManIndex=db.sillokManIndex
sillokManInfo = db.sillokManInfo
akssillokJoined = db.akssillokJoined
sillokIntegrated=sdb.sillokIntegrated

with open('lunar2sol.json','r') as f:
    lunar2sol=json.load(f)


def main():
    for i in sillokIntegrated.find():
        if int(i['date'].split('-')[0])>=1896:
            soldate=i['date'].replace('L0','')
            sillokIntegrated.update_one({'_id':i['_id']},{"$set":{'soldate':soldate}})
        else:
            lunardate=i['date']
            try:
                soldate=lunar2sol[lunardate]
                # print(soldate)
            except:
                print(i['date'])
                continue

            sillokIntegrated.update_one({'_id':i['_id']},{"$set":{'soldate':soldate}})


    # #1896년부터 양력 도입
    # for i in sillokManInfo.find({'date':{"$exists":1}}):
    #
    #     year=int(i['date'].split('-')[0])
    #
    #     if year<1896:
    #         try:
    #             lunardate=i['date']
    #             soldate=lunar2sol[lunardate]
    #         except Exception as e:
    #             print(e)
    #             print(i)
    #
    #         sillokManInfo.update_one({'_id':i['_id']},{"$set":{'soldate':soldate}})
    #         print(soldate)
    #
    #     elif year>=1896:
    #         soldate=i['date'].replace('L0','')
    #         sillokManInfo.update_one({'_id':i['_id']},{"$set":{'soldate':soldate}})
    #         print(soldate)
    #     else:
    #         print("else")
    #         print(i['date'])





def wrongDate():
    #1727년 3월은 29일까지지만, 3월 30일까지로 잘못기록되어 그 다음 달인 윤 3월이 전부 1일씩 뒤로 밀림
    wrong1=[i for i in sillokManInfo.find({"date":'1727-03-30L0'})]
    for i in wrong1:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1727-03-01L1"}})
    wrong2=[i for i in sillokManInfo.find({"date":{"$exists":1}}) if i['date'][0:7]=='1727-03' and "L1" in i['date']]
    for i in wrong2:
        ndate=i['date'][0:8]+"{0:0>2}".format(str(int(i['date'].split('-')[2][:2])+1))+i['date'][10::]
        print(ndate)
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':ndate}})
    #1430년 4월은 하루씩 밀려서 기록됨. 즉 4월 3일은 원래는 4월 2일이 맞음.
    m4l0=[i for i in sillokManInfo.find({"date":{"$exists":1}}) if i['date'][0:7]=='1430-04']
    for i in m4l0:
        ndate=i['date'][0:8]+"{0:0>2}".format(str(int(i['date'].split('-')[2][:2])-1))+i['date'][10::]
        print(ndate)
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1727-03-01L1"}})

    #1498년 11월은 29일까지지만, 11월 30일까지로 잘못기록되어 그 다음 달인 윤 11월이 전부 1일씩 뒤로 밀림
    m11d29=[i for i in sillokManInfo.find({"date":'1498-11-30L0'})]
    for i in m11d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1498-11-01L1"}})
    m11l1=[i for i in sillokManInfo.find({"date":{"$exists":1}}) if i['date'][0:7]=='1498-11' and "L1" in i['date']]
    for i in m11l1:
        ndate=i['date'][0:8]+"{0:0>2}".format(str(int(i['date'].split('-')[2][:2])+1))+i['date'][10::]
        print(ndate)
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':ndate}})
    #1513년 4월 30일 없음 1513년 4월 29일이 맞음
    m4d29=[i for i in sillokManInfo.find({"date":'1513-04-30L0'})]
    for i in m4d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1513-04-29L0"}})
    #1517년 7월 30일 없음 1517년 7월 29일이 맞음
    m7d29=[i for i in sillokManInfo.find({"date":'1517-07-30L0'})]
    for i in m7d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1517-07-29L0"}})

    #1530년 2월은 전체 달력이 하루씩 -1해줘야함
    m2d29=[i for i in sillokManInfo.find({"date":'1530-02-01L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1530-01-30L0"}})
    m2l1=[i for i in sillokManInfo.find({"date":{"$exists":1}}) if i['date'][0:7]=='1530-02']
    for i in m2l1:
        ndate=i['date'][0:8]+"{0:0>2}".format(str(int(i['date'].split('-')[2][:2])-1))+i['date'][10::]
        print(ndate)
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':ndate}})
    #1597년 9월은 전체 달력을 하루씩 -1해줘야함
    m2d29=[i for i in sillokManInfo.find({"date":'1597-09-01L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1597-08-30L0"}})
    m2l1=[i for i in sillokManInfo.find({"date":{"$exists":1}}) if i['date'][0:7]=='1597-09']
    for i in m2l1:
        ndate=i['date'][0:8]+"{0:0>2}".format(str(int(i['date'].split('-')[2][:2])-1))+i['date'][10::]
        print(ndate)
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':ndate}})
    #1687년 3월 31일 없음. 4월 2일이 맞음.
    m2d29=[i for i in sillokManInfo.find({"date":'1687-03-31L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1687-04-02L0"}})
    #1839년 6월 29일, 30일은 각각 -1씩 해줘야함
    m2d29=[i for i in sillokManInfo.find({"date":'1839-06-29L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1839-06-28L0"}})
    m2d29=[i for i in sillokManInfo.find({"date":'1839-06-30L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1839-06-29L0"}})
    #1858년 1월 30일 없음 29일이 맞음
    m2d29=[i for i in sillokManInfo.find({"date":'1858-01-30L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1858-01-29L0"}})
    #1869년 4월 30일 없음 29일이 맞음
    m2d29=[i for i in sillokManInfo.find({"date":'1869-04-30L0'})]
    for i in m2d29:
        sillokManInfo.update_one({"_id":i['_id']},{'$set':{'date':"1869-04-29L0"}})

main()
