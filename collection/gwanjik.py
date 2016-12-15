import requests

from lxml import html
import random
import pymongo

client = pymongo.MongoClient('143.248.156.197')
#client = pymongo.MongoClient('localhost')

db = client.sillok

url = 'http://encysillok.aks.ac.kr/Theme/GwanJik'
AGENT = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
         "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
         ]

session = requests.Session()
session.headers.update({
    'User-Agent': AGENT[random.randint(0, 3)],
})
page = session.get(url).content
article = html.fromstring(page)
print(article.text)
paragraph =[i.text for i in article.xpath('(//div')]
print(paragraph)