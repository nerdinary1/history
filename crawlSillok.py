import requests
from lxml import html
import random
import pymongo

client = pymongo.MongoClient('143.248.156.197')
#client = pymongo.MongoClient('localhost')

db = client.sillok

url_basic = 'http://sillok.history.go.kr/id/'
AGENT = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
         "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
         ]

session = requests.Session()
session.headers.update({
    'User-Agent': AGENT[random.randint(0, 3)],
})
kings = {
        '태조':'kaa',
         '정종':'kba',
         '태종':'kca',
         '세종':'kda',
         '문종':'kea',
         '단종':'kfa',
         '세조':'kga',
         '예종':'kha',
         '성종':'kia',
         '연산군':'kja',
         '중종':'kka',
         '인종':'kla',
         '명종':'kma',
         '선조':'kna',
         '선조(수정)':'knb',
         '광해군':'koa',
         '광해군(정초)':'kba',
         '인조':'kpa',
         '효종':'kqa',
         '현종':'kra',
         '현종(개수)':'krb',
         '숙종':'ksa',
         '경종':'kta',
         '경종(수정)':'ktb',
         '영조':'kua',
         '정조':'kva',
         '순조':'kwa',
         '헌종':'kxa',
         '철종':'kya',
         '고종':'kza',
         '순종':'kzb'
         }
collectionList= list(kings.values())

for collectionName in collectionList:
    urls = [i['_id'] for i in db[collectionName].find()]
    for url in urls:
        page = session.get(url).content
        article = html.fromstring(page)
        db[collectionName].insert({'_id':url},{
                        'paragraph':"".join([i.text for i in article.cssselect('div.ins_view_in.ins_left_in div.ins_view_pd p.paragraph')]),
                                                })


