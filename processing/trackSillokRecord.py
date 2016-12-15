import pymongo
import sys
import csv
import os
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research
sdb=client.sillok

aksManIndex=db.aksManIndex
aksManInfo=db.aksManInfo
collection = db.sillokManInfo
sillokManIndex=db.sillokManIndex
sillokManInfo = db.sillokManInfo
akssillokJoined = db.akssillokJoined
sillokIntegrated = sdb.sillokIntegrated



def makeFile():
    persons = sillokManIndex.find()
    for person in persons:
        with open('./trackRecord/'+person['nameIndex']+'_'+person['이름']+'.txt', 'w') as f:
            records=[i for i in sillokIntegrated.find({"nameIndex":{"$in":[person['nameIndex']]}})]
            records.sort(key=lambda k: k['date'])
            for i in person:
                if i in ['_id', 'ref']:
                    continue
                f.write(i)
                f.write(' : ')
                f.write(str(person[i]))
                f.write(', ')
            f.write('\n')
            for record in records:
                f.write(record['date'])
                f.write('\n')



def makeCountFile():
    persons = sillokManIndex.find()
    with open('namecount.csv','w') as f:
        fieldnames=['name','count']
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for person in persons:
            records=[i for i in sillokIntegrated.find({"nameIndex":{"$in":[person['nameIndex']]}})]
            records.sort(key=lambda k: k['date'])
            rdict={}
            rdict['name']=person['nameIndex']+'_'+person['이름']
            rdict['count']=len(records)
            writer.writerow({'name':rdict['name'],'count':rdict['count']})


makeFile()
