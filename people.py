from selenium import webdriver
import random
import pymongo
import time
import re

client = pymongo.MongoClient('143.248.156.197')
db=client.research
collection= db.aksPeople
URL = 'http://people.aks.ac.kr/front/dirSer/exm/exmKingExmList.aks?classCode=MN&className=문과&isEQ=true&kristalSearchArea=P'
driver= webdriver.Chrome(executable_path='/Users/choimarco/chromedriver')
def getTestList():
    url = URL
    driver.get(url)
    kings = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('[headers="king_name"] a')]
    wholeTests = []
    for king in kings:
        driver.get(king)
        tests = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('[headers="king_name"] a')]
        wholeTests.append(tests)
        time.sleep(1)
        break

    return wholeTests

def getInformation(passed):
    driver.get(passed)
    name = driver.find_element_by_css_selector('#contentBody_title').text
    examInfo=driver.find_element_by_css_selector('h4#exmInfo').text
    examInfo=examInfo.split()
    affillation = examInfo[0].strip('[]')
    kingname = re.sub(r'\([^)]*\)','',examInfo[1])
    year=examInfo[2].split('(')[1].replace(')','')
    type = re.sub(r'\([^)]*\)','',examInfo[4])
    grade = re.sub(r'\([^)]*\)','',examInfo[5])
    ranking = re.sub(r'\([^)]*\)','',examInfo[6]).split('(')[1].replace(")","").split("/")[0]
    totalpassed = re.sub(r'\([^)]*\)','',examInfo[6]).split('(')[1].replace(")","").split("/")[1]
    personSummaryItem=[i.text for i in driver.find_elements_by_xpath('//div[@id="exm"]/div[1]//td[@class="first"]')]
    personSummaryContent=[i.text for i in driver.find_elements_by_xpath('//div[@id="exm"]/div[1]//tr//td[2]')]
    firstTable = [i for i in zip(personSummaryItem,personSummaryContent)]


    print(kingname)

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
            getInformation(passed)
            break

