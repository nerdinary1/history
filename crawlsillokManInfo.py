import pymongo
import time
import sys
import requests
from lxml import html
from kings import kings
import datetime
basic = 'http://sillok.history.go.kr/manInfo/popManDetail.do?manId='
session = requests.Session()


#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient()

db=client.research
sdb= client.sillok
sillokManInfo = db.sillokManInfo
sillokManURL = db.sillokManURL
sillokManURLUnique = db.sillokManURLUnique


def save(basic_category,basic_info, relative,url):

    if len(relative) ==0:
        sillokManInfo.insert({"url":url})
        for category,info in zip(basic_category,basic_info):
            if info.isdigit():
                info = int(info)
            sillokManInfo.update_one({"url":url}, {"$set":{category:info}})

    for i in relative:

        if i[3].isdigit():

            sillokManInfo.insert(
                {
                    'url':url,
                    '왕대':i[0],
                    '왕력':int(i[1]),
                    '년':int(i[2]),
                    '월':int(i[3]),
                    '일':int(i[4]),
                    '관력':i[5],
                    '형태':i[6],
                    '이름':basic_info[0]
                }
            )
        else:
            sillokManInfo.insert(
                {
                    'url':url,
                    '왕대':i[0],
                    '왕력':int(i[1]),
                    '년':int(i[2]),
                    '월':i[3],
                    '일':int(i[4]),
                    '관력':i[5],
                    '형태':i[6],
                    '이름':basic_info[0]
                }
            )


        for category,info in zip(basic_category,basic_info):
            if info.isdigit():
                info = int(info)

            sillokManInfo.update_many({'url':url}, {"$set":{category:info}})


def setup(name):
    url = name
    page = html.fromstring(session.get(url).content)
    basic_category = page.xpath('//table[@class="tbl_type01 tbl_view"]/tbody//th/text()')
    basic_info = [str(i.text).replace('None',"").strip('\r\n\t')for i in page.xpath('//table[@class="tbl_type01 tbl_view"]/tbody//tr/td')]

    relnum = int(len(page.xpath('//table[@class="tbl_type01"]/tbody/tr/td'))/8)
    relative = []
    for i in range(1,relnum+1):
        tem=[i.replace('\r','').replace('\n','').replace('\t','') for i in page.xpath('//table[@class="tbl_type01"]/tbody/tr['+str(i)+']/td[position()<8]/text()')]
        relative.append(tem)

    save(basic_category,basic_info, relative,url)

def countPerson():
     persons = {i['url'] for i in sillokManInfo.find()}
     print(len(persons))



#new ..
def collectPersonURL():
    collectionList=kings
    for collection in collectionList:
        for article in sdb[collection].find({}, no_cursor_timeout=True):
            for nameIndex in article['nameIndex']:

                sillokManURL.insert(
                    {
                        "url":basic+nameIndex
                    }
                )

        print(collection)

def treatPersonURL():

    before=time.time()
    allURL=set([i['url'] for i in sillokManURL.find()])
    for i in allURL:
        sillokManURLUnique.insert(
            {
                "_id":i
            }
        )
    after=time.time()
    print(after-before)


def missingsillokManInfo():
    nameList = [i['_id'] for i in sillokManURLUnique.find()]
    infoList = list(set([i['url'] for i in sillokManInfo.find()]))
    uncrawled=[]
    for name in nameList:
        if name not in infoList:
            print(name)
            uncrawled.append(name)
    return uncrawled

# sillokManURLUnique = db.sillokManURLUnique
# cnt=22752
# l = [i["_id"] for i in sillokManURLUnique.find({})]
# for i in l[22753::]:
#     cnt+=1
#     setup(i)
#     print(cnt)
def main(l,start,end):

    cnt=0
    #번호를 db 순서 기준으로 잡음. ex) db:26401 -> 리스트에서도 26401

    for i in l[start-1:end:]:
        try:
            setup(i)
            now = l.index(i)+1
            print(now)
        except Exception as e :
            print(e)
            time.sleep(10)
            sillokManInfo.delete_many({"url":i})
            setup(i)
            now = l.index(i) + 1
            print(now)
def delete(start,end):
    l = [i["_id"] for i in sillokManURLUnique.find({})]
    for i in l[start - 1:end:]:

            sillokManInfo.delete({"url": i})

            now = l.index(i) + 1
            print(now)
l = [i['_id'] for i in sillokManURLUnique.find()]

# length = int(len(l)/6)
# main(l,3*length+1,4*length)
# main(l,4*length+1,5*length)
main(missingsillokManInfo(),1,2)

#main(26402,30000)
#main(30001,40000)
#main(40001,50000)
#main(50000,62600)
# db=client.research
# sillokManURLUnique = db.sillokManURLUnique
# sillokManInfo=db.sillokManInfo
# sillokManInfo.delete_many({"url":"http://sillok.history.go.kr/manInfo/popManDetail.do?manId=M_0005134"})

# l=missingsillokManInfo()
# print(len(l))

