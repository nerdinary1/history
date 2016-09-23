import os
import pymongo
from lxml import etree

client = pymongo.MongoClient('143.248.156.197')
#client = pymongo.MongoClient('localhost')

db=client.sillok
from lxml.cssselect import CSSSelector
file_list=[]
for root, dirs, files in os.walk('data/'):
    for file in files:
        if '.xml' in file and file[-7] =='1':
            file_list.append(file)


for file in file_list:
    doc = etree.parse('data/'+file)
    # doc=etree.parse('data/2nd_waa_106.xml')
    articles = doc.xpath('//level5/@id')
    print(file)
    for article in articles:
        xpathBase='//level5[@id="'+article+'"]'
        king = str(doc.xpath(xpathBase+'/..//dateOccured[@type="재위연도"]')[0].text).split(' ')[0]
        url = 'http://sillok.history.go.kr/id/k'+str(article)[1::]
        title = doc.xpath(xpathBase+'//title//mainTitle')[0].text
        date = str(doc.xpath(xpathBase+'//dateOccured/@date')[0])
        subject=[str(i.text) for i in doc.xpath(xpathBase+'//subjectClass')]
        original = "".join([i for i in doc.xpath(xpathBase+'//content//paragraph/text()') if '\n' not in i])
        names = [i.text for i in doc.xpath(xpathBase+'//text/content/paragraph/index[@type="이름"]')]
        nameIndex= [str(i) for i in doc.xpath(xpathBase+'//text/content/paragraph/index[@type="이름"]/@ref')]
        places = [i.text for i in doc.xpath(xpathBase+'//text/content/paragraph/index[@type="지명"]')]
        placeIndex= [str(i) for i in doc.xpath(xpathBase+'//text/content/paragraph/index[@type="지명"]/@num')]
        books = [i.text.replace('《','').replace('》','') for i in doc.xpath(xpathBase+'//text/content/paragraph/index[@type="서명"]')]
        bookIndex= [str(i) for i in doc.xpath(xpathBase+'//text/content/paragraph/index[@type="서명"]/@num')]

        collection = 'k'+str(article)[1:3]
        db[collection].insert({
            'king':king,
            '_id':url,
            'title':title,
            'date':date,
            'subject':subject,
            'original':original,
            'names':names,
            'places':places,
            'books':books,
            'nameIndex':nameIndex,
            'placeIndex':placeIndex,
            'bookIndex':bookIndex
        })