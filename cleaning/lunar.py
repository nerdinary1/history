
from urllib.parse import urlencode
import random
import re
import requests
from lxml import html
import json
import time
URL = "http://astro.kasi.re.kr/Life/Knowledge/solar2lunar/convert_monthly.php"
AGENT = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
         "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
         ]
data = {"sol_year": None, "sol_month": None}

session=requests.Session()
session.headers.update({"Content-Type": "application/x-www-form-urlencoded",
"Accept":"text/html"})
session.headers.update({
    'User-Agent': AGENT[random.randint(0, 3)],
})

def solar2lunar(year=1425,month=8):
    data["sol_year"] = year
    data["sol_month"] = month
    try:
        resp=session.post(URL,data=urlencode(data))
    except:
        time.sleep(5)
        resp=session.post(URL,data=urlencode(data))
    resp.encoding='cp949'


    p=html.fromstring(resp.text)
    rc=re.compile(r'\d{4}-\d{2}-\d{2}.*')

    sol_dates=[i.pop().split()[0] for i in (rc.findall(i.text) for i in p.xpath('//tr/td[not(@colspan="4")][1]'))]
    lun_dates=[]
    for i in p.xpath('//tr/td[not(@colspan="4")][2]'):
        for j in rc.findall(i.text):

            if "윤" in j:
                j=j.split(' ')[0]+"L1"
                print(j)

            else:
                j=j+"L0"
            lun_dates.append(j)

    return lun_dates, sol_dates

def datesave(lun_dates,sol_dates):
    datedict={}

    for i in zip(lun_dates,sol_dates):
        datedict[i[0]]=i[1]

    with open('bdate.json','a') as f:
        json.dump(datedict,f)
        f.write(',')
def main():

    startyear=1391
    startmonth=1
    with open('bdate.json','a') as f:
        f.write('[')
    for year in range(startyear,2017):
        for month in range(startmonth,13):
            print(year,month)
            r=solar2lunar(year,month)
            datesave(r[0],r[1])
        with open('bdate.json','a') as f:
            f.write(']')


# main()
with open('bdate.json','r') as f:
    data= json.load(f)

lunar2soldic={}
with open('lunar2sol.json','w') as f:
    for dic in data:
        lunar2soldic.update(dic)
    json.dump(lunar2soldic,f)
sol2lunardic={}
with open('sol2lunar.json','w') as f:
    for k, v in lunar2soldic.items():
        sol2lunardic[v]=k
    json.dump(sol2lunardic,f)