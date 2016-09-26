import pymongo
import time
import sys
import requests
from lxml import html
basic = 'http://sillok.history.go.kr/manInfo/popManDetail.do?manId='
session = requests.Session()


#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')

db=client.research
sdb= client.sillok
collection = db.sillokPeople

def save(basic_category,basic_info, relative,url):

    if len(relative) ==0:
        collection.insert({"url":url})
        for category,info in zip(basic_category,basic_info):
            if info.isdigit():
                info = int(info)
            collection.update_one({"url":url},{"$set":{category:info}})

    for i in relative:

        if i[3].isdigit():

            collection.insert(
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
            collection.insert(
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

            collection.update_many({'url':url},{"$set":{category:info}})


def setup(name):
    url = basic+name
    page = html.fromstring(session.get(url).content)
    basic_category = page.xpath('//table[@class="tbl_type01 tbl_view"]/tbody//th/text()')
    basic_info = [i.strip('\r\n\t')for i in page.xpath('//table[@class="tbl_type01 tbl_view"]/tbody//tr/td/text()')]
    if len(basic_info[0]) == 0:
        print('No such a person. Continue ',name)
        return

    relnum = int(len(page.xpath('//table[@class="tbl_type01"]/tbody/tr/td'))/8)
    relative = []
    for i in range(1,relnum+1):
        tem=[i.replace('\r','').replace('\n','').replace('\t','') for i in page.xpath('//table[@class="tbl_type01"]/tbody/tr['+str(i)+']/td[position()<8]/text()')]
        relative.append(tem)

    save(basic_category,basic_info, relative,url)

def countPerson():
     persons = {i['url'] for i in collection.find()}
     print(len(persons))


def main():
    collectionList=sdb.collection_names()
    # nameSet=set()
    for collection in collectionList:
        for article in sdb[collection].find({},no_cursor_timeout=True):
            for name in article['nameIndex']:
                try:
                    setup(name)
                except:
                    time.sleep(5)
        # allnames=[i['nameIndex'] for i in sdb[collection].find() if len(i['nameIndex'])>0]
        # for names in allnames:
        #     nameSet.update(set(names))
    # nameList = list(nameSet)
    #
    # for name in nameList:
    #     try:
    #         setup(name)
    #     except:
    #         time.sleep(5)



main()