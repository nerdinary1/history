import pymongo
import csv
import sys
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')
def wholeData():
    db=client.research
    sillokFirstEmergence=db.sillokFirstEmergence
    fieldnames= ['계열','level','이름','생년','졸년','본관','왕명','합격년도','합격연령','순위','응시인원','시험유형','실록최초등장','gap']
    with open('FirstEmergence.csv','w') as csvfile:
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        d=dict()
        for i in fieldnames:
            d[i]=""
        for i in sillokFirstEmergence.find():
            empty_d=d
            empty_d['gap'] = int(i['실록최초등장'])-int(i['합격년도'])
            keys=list(i.keys())
            for key in keys:
                if key in fieldnames:
                    empty_d[key] = i[key]
            full_d=empty_d

            writer.writerow(full_d)
def makeCSV(collectionname):
    db=client.research
    collection=db[collectionname]
    fieldnames=set()
    for doc in collection.find():
        fieldnames.update(set(doc.keys()))
    fieldnames= list(fieldnames)

    with open(collectionname+'.csv','w') as csvfile:
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        d=dict()
        for i in fieldnames:
            d[i]=""
        for i in collection.find():
            empty_d=d
            keys=list(i.keys())
            for key in keys:
                if key in fieldnames:
                    empty_d[key] = i[key]
            full_d=empty_d

            writer.writerow(full_d)

makeCSV("sillokManInfo")