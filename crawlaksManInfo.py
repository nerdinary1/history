from selenium import webdriver
import sys
import pymongo
import time
import re

#Mac에서 실행
if sys.platform =="darwin":
    client = pymongo.MongoClient('143.248.156.197')
    driver= webdriver.Chrome(executable_path='/Users/choimarco/chromedriver')
#window에서 실행
else:
    client = pymongo.MongoClient('localhost')
    driver = webdriver.Chrome(executable_path="C:\\Users\\DH CHOI\\chromedriver")

db=client.research
aksManInfo= db.aksManInfo

# URL = 'http://people.aks.ac.kr/front/dirSer/exm/exmKingExmList.aks?classCode=MN&className=문과&isEQ=true&kristalSearchArea=P'
URL = 'http://people.aks.ac.kr/front/dirSer/exm/exmKingExmList.aks?classCode=MU&className=무과&isEQ=true&kristalSearchArea=P'

def getTestList():
    url = URL
    driver.get(url)
    kings = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('[headers="king_name"] a')]
    wholeTests = []
    for king in kings[19:21]:
        driver.get(king)
        tests = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('[headers="king_name"] a')]
        wholeTests.append(tests)
        time.sleep(1)


    return wholeTests

def getInformation(passed):
    driver.get(passed)
    name = driver.find_element_by_css_selector('#contentBody_title').text
    # name = re.sub(r'\([^)]*\)','',name)
    examInfo=driver.find_element_by_css_selector('h4#exmInfo').text
    examInfo=examInfo.split()

    try:
        affillation = examInfo[0].strip('[]')
        kingname = re.sub(r'\([^)]*\)','',examInfo[1])
        year=int(examInfo[2].split('(')[1].replace(')',''))
        type = re.sub(r'\([^)]*\)','',examInfo[4])
        grade = re.sub(r'\([^)]*\)','',examInfo[5])
        ranking = int(examInfo[6].split('(')[1].replace(")","").split("/")[0])
        totalpassed = int(examInfo[6].split('(')[1].replace(")","").split("/")[1])

    #고종 이후
    except:
        try:
            affillation = examInfo[0].strip('[]')
            kingname = re.sub(r'\([^)]*\)','',examInfo[1])
            year=int(examInfo[2].split('(')[1].replace(')',''))
            type = re.sub(r'\([^)]*\)','',examInfo[4])
            ranking = int(examInfo[5].split('(')[1].replace(")","").split("/")[0])
            totalpassed = int(examInfo[5].split('(')[1].replace(")","").split("/")[1])
            grade =""
        #문과 예외처리
        except:
            affillation = examInfo[0].strip('[]')
            kingname = re.sub(r'\([^)]*\)','',examInfo[1])
            year=int(examInfo[2].split('(')[1].replace(')',''))
            type = re.sub(r'\([^)]*\)','',examInfo[4])
            grade =""
            ranking = ""
            totalpassed=""


    personSummaryItem=[i.text for i in driver.find_elements_by_xpath('//div[@id="exm"]/div[1]//td[@class="first"]')]
    personSummaryContent=[i.text for i in driver.find_elements_by_xpath('//div[@id="exm"]/div[1]//tr//td[2]')]
    firstTable = [i for i in zip(personSummaryItem,personSummaryContent)]
    personCareerItem=[i.text for i in driver.find_elements_by_xpath('(//table[@class="xml_table"])[3]//td[@class="first"]')]
    personCareerContent=[i.text for i in driver.find_elements_by_xpath('(//table[@class="xml_table"])[3]//td[2]')]
    secondTable=[i for i in zip(personCareerItem,personCareerContent)]
    return name, affillation, kingname, year, type, grade, ranking, totalpassed, firstTable, secondTable

def saveInformation(returns):

    insertresult=aksManInfo.insert({
        "이름":returns[0],
        "계열":returns[1],
        "왕명":returns[2],
        "합격년도":returns[3],
        "시험유형":returns[4],
        "합격등급":returns[5],
        "순위":returns[6],
        "응시인원":returns[7],
        })

    for i in returns[8]:
        i=list(i)
        if "주1" in i[1]:
            i[1] = i[1].replace("(주1)","")
        if "주2" in i[1]:
            i[1] = i[1].replace("(주2)","")
        aksManInfo.find_one_and_update({"_id":insertresult},{"$set":{i[0]:i[1]}})
    person = aksManInfo.find_one({"_id":insertresult})
    try:
        birthyear = person["birth"]
        birthyear = int(birthyear.split()[1].split('년')[0])
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"birth":birthyear}})
    except:
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"birth":0}})
    try:
        deathyear = person["졸년"]
        deathyear = int(deathyear.split()[1].split('년')[0])
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"졸년":deathyear}})
    except:
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"졸년":0}})
    try:
        hometown = person["본관"]
        hometown = re.sub(r'\([^)]*\)','',hometown)
        if hometown=="미상":
            aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"본관":""}})
        else:
            aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"본관":hometown}})
    except:
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"본관":""}})
    try:
        passage=person["합격연령"]
        passage = int(passage.replace("세",''))
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"합격연령":passage}})
    except:
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"합격연령":0}})
    try:
        deathage=person["향년"]
        deathage = int(deathage.replace("세",''))
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"향년":deathage}})
    except:
        pass

    try:
        habitat=person["거주지"]
        habitat =re.sub(r'\([^)]*\)','',habitat)
        aksManInfo.find_one_and_update({"_id":insertresult}, {"$set":{"거주지":habitat}})
    except:
        pass

    for i in returns[9]:
        if i[0] =="관직":
            aksManInfo.find_one_and_update({"_id":insertresult},{"$push":{"관직":i[1]}})



wholeTests=getTestList()

for tests in wholeTests:
    for test in tests:
        driver.get(test)
        time.sleep(3)
        l=driver.find_element_by_css_selector('select#page_per_num option:nth-child(3)')
        driver.execute_script("arguments[0].value='10000';",l)
        driver.find_element_by_css_selector('select#page_per_num option:nth-child(3)').click()
        passeds = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('[headers="fullname"] a')]

        for passed in passeds:
            saveInformation(getInformation(passed))
anonymous=[i['_id'] for i in aksManInfo.find({"UCI":{"$exists":0}})]
for i in anonymous:
    num=str(anonymous.index(i)+1)
    aksManInfo.update_one({"_id":i},{"$set":{"UCI":"anonymous"+num}})