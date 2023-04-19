import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

def toCSV(name, classes):
    with open (name, 'w') as output:
        writer = csv.writer(output)
        for item in classes:
            row = []
            row.append(item)
            courses = classes[item]
            for course in courses:
                row.append(course)
            writer.writerow(row)


def checkXPATH(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def getCode(i):
    code_xpath = f"/html/body/div[3]/div[2]/div/div/div/div[{i}]/div[1]/span[1]/strong"
    code_xpath_secondary = f"/html/body/div[3]/div[2]/div/div/div/div[{i}]/div[1]/span[2]/strong"
    if checkXPATH(code_xpath):
        code = driver.find_element(By.XPATH, code_xpath)
        code = code.text.replace(".", "")
    else:
        code = driver.find_element(By.XPATH, code_xpath_secondary)
        code = code.text.replace(".", "")
    return code


def removeOr(text):
    if "or" in text:
        text.replace(" or " , "/")
    return text

def removeComma(text):
    if "," in text:
        text.replace(",", "")
    return text

def removeAnd(text):
    if "and" in text:
        text.replace(" and", "")
    return text

def removeComma(text):
    if "." in text:
        text.replace(".", "")
    return text


def addCoreReqs(programs):
    class_reqs: dict[str, list[str]] = {}
    for program in programs:
        if program == 'PHARMACY  (NON-DEPARTMENTAL) (PHCY)':
            link = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[1]/div[2]/ul[16]/li[9]/a')
            link.click()
        else:
            link = driver.find_element(By.PARTIAL_LINK_TEXT, program)
            link.click()

        all_courses = driver.find_elements(By.CLASS_NAME, "courseblock")

        i = 1
        for course in all_courses:
            course_code = getCode(i)
            req_path = f'/html/body/div[3]/div[2]/div/div/div/div[{i}]/div[7]/span'

            if (checkXPATH(req_path)):
                all_reqs = driver.find_element(By.XPATH, req_path)
                req_text = all_reqs.text.lower()

                co_presence = req_text.find("corequisite")
                co_presence2 = req_text.find("co-requisite")

                if (co_presence != -1 or co_presence2 != -1):
                    class_reqs[course_code] = []
                    if (co_presence != -1):
                        index = co_presence + 12
                        req_text = req_text[index:]
                    elif (co_presence2 != -1):
                        index = co_presence + 13
                        req_text = req_text[index:]
                    
                    if req_text[0] == ",":
                        req_text = req_text[1:]
                    else:
                        req_text = req_text[0:]

                    if req_text.find(";") != -1:
                        req_text = req_text[:req_text.find(";")]

                    
                    class_reqs[course_code] = req_text.upper()

            i += 1

        driver.get(url)

    return class_reqs


url = "https://catalog.unc.edu/courses/"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
total = soup.find("div", {"id" : "atozindex"})
headings = total.find_all("li")

programs = []
degree_raw = []
count = 0
for heading in headings:
    program = heading.text
    if len(program) > 2:
        programs.append(heading.text)
        degree_raw.append(heading)

driver = webdriver.Chrome()
driver.get(url)


class_reqs = addCoreReqs(programs)
toCSV('output3.csv', class_reqs)

driver.quit()