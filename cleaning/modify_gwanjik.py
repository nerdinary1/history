import pymongo
import sys
import time
import pandas as pd
from bson.son import SON
import numpy as np
import re
import json
#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research
sillokManIndex=db.sillokManIndex_new
sillokManInfo = db.sillokManInfo
# akssillokJoined = db.akssillokJoined
# with open('../collection/gwanjikdictionary_by_buseo.json','r') as f:
#     table=json.load(f)
#
# depts=[]
# for dept in table:
#     depts.append(dept['department'])
# depts=set(depts)
# print(depts)
#
# #이조참판(한자)->이조(한자) 참판(한자)
# hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
#
# cnt=0
# for man in sillokManIndex.find({"career":{"$exists":1}}):
#     careers=man['career']
#     newcareers=[]
#
#     for career in careers:
#         if career==None:
#             newcareers.append(career)
#             continue
#         hancareer=hangul.sub("",career)
#         tmp=[]
#         for dept in depts:
#
#             handept=hangul.sub("",dept)
#             deptmatch=re.compile(handept+r'\w+\([^-\s].*')
#
#             if True:
#                 try:
#                     deptmatch.match(career).group()
#                 except:
#                     continue
#
#                 newcareer=career.replace(handept,dept+' ')
#                 first=newcareer.split(' ')[0]
#                 second=newcareer.split(' ')[1]
#
#                 target=re.search(r'\([^)]*\)',first).group()
#                 second=second.replace(target,'')
#                 newcareer=first+' '+second
#                 print(newcareer)
#                 newcareers.append(newcareer)
#                 tmp.append(newcareer)
#         if len(tmp)==0:
#             newcareers.append(career)
#     print(newcareers)

#     sillokManIndex.update_one({'_id':man['_id']},
#                               {'$set':{'career':newcareers}})

# #이조참판(한자)->이조(한자) 참판(한자) in sillokManInfo
# hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
#
# cnt=0
# for man in sillokManInfo.find({"관력":{"$exists":1}}):
#     career=man['관력']
#     newcareers=[]
#
#     if career==None:
#         newcareers.append(career)
#         continue
#
#     hancareer=hangul.sub("",career)
#
#     for dept in depts:
#
#         handept=hangul.sub("",dept)
#         deptmatch=re.compile(handept+r'\w+\([^-\s].*')
#
#         if True:
#             try:
#                 deptmatch.match(career).group()
#             except:
#                 continue
#             newcareer=career.replace(handept,dept+' ')
#             first=newcareer.split(' ')[0]
#             second=newcareer.split(' ')[1]
#
#             target=re.search(r'\([^)]*\)',first).group()
#             second=second.replace(target,'')
#             newcareer=first+' '+second
#             print(newcareer)
#
#
#             sillokManInfo.update_one({'_id':man['_id']},
#                                       {'$set':{'관력':newcareer}})
# #delete gwanjik special characters in sillokManIndex
# sc=re.compile(r'[-·/ ]')
# for man in sillokManIndex.find({"career":{"$exists":1}}):
#     careers=man['career']
#     newcareers=[]
#     for career in careers:
#         if career == None:
#             newcareers.append(None)
#             continue
#         newcareers.append(sc.sub('',career))
#
#     sillokManIndex.update_one({"_id":man['_id']},{"$set":{"career":newcareers}})
#
# #delete gwanjik special characters in sillokManInfo
# sc=re.compile(r'[-·/ ]')
# for man in sillokManInfo.find({"관력":{"$exists":1}}):
#     career=man['관력']
#     newcareer=sc.sub('',career)
#     sillokManInfo.update_one({"_id":man['_id']},{"$set":{"관력":newcareer}})

def modify_gwanjik(correct,shouldhaves,shouldnthaves):

    for man in sillokManIndex.find({"career":{"$exists":1}}):
        careers=man['career']
        print(careers)
        newcareers=[]
        for career in careers:
            tmp=[]
            if None==career:
                newcareers.append(career)
                continue
            for shouldhave in shouldhaves:
                if shouldhave in career:
                    for shouldnthave in shouldnthaves:
                        if shouldnthave not in career:
                            tmp.append(correct)
                            newcareers.append(correct)
            if len(tmp) ==0:
                newcareer=career
            newcareers.append(newcareer)
        print(newcareers)
        # sillokManIndex.update_one({"_id":man['_id']},{"$set":{"career":newcareers}})

def strictly_modify_gwanjik(target, correct):
    cnt=0
    for man in sillokManIndex.find():
        careers=man['career']
        newcareers=[]
        for career in careers:
            tmp=[]
            if None==career:
                newcareers.append(career)
                continue
            if career == target:
                tmp.append(correct)
                newcareers.append(correct)
            if len(tmp) ==0:
                newcareers.append(career)
        r = sillokManIndex.update_one({"_id":man['_id']},{"$set":{"career":newcareers}})
        print(r)
        cnt=cnt+r.modified_count
    print(cnt)


# modify_gwanjik('사헌부(司憲府) 지평(持平)',shouldhaves=['지평('],shouldnthaves=['장무지평(掌務持平)'])

strictly_modify_gwanjik("간원정언(諫院正言)", "사간원(司諫院) 정언(正言)")
strictly_modify_gwanjik("정언(正言)", "사간원(司諫院) 정언(正言)")
strictly_modify_gwanjik("우의정(古議政)","의정부(議政府) 우의정(右議政)")
strictly_modify_gwanjik("좌의정(右議政)","의정부(議政府) 좌의정(左議政)")
strictly_modify_gwanjik("장령(將領)","사헌부(司憲府) 장령(掌令)")
strictly_modify_gwanjik("집의(執儀)","사헌부(司憲府) 집의(執義)")