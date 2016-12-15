import pymongo
import json
import re

client=pymongo.MongoClient('143.248.156.197')
db=client.sillok
sillokIntegrated=db.sillokIntegrated_new

def makeIntegrated():
    collist= db.collection_names()
    for col in collist:
        for i in col.find():
            sillokIntegrated.insert(i)


yearset={}
for i in sillokIntegrated.find({},{'_id':1,'date':1}):
    rc=re.compile(r'\D{3}_\d{3}')
    try:
        yearkey=rc.findall(i['_id']).pop()
        yearvalue=i['date'][0:4]
        yearset[yearkey]=yearvalue
    except:
        continue

with open('yearconvert.json','w') as f:
    json.dump(yearset,f)

