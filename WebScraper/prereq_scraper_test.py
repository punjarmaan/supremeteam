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


def addReqs(programs):
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
                class_reqs[course_code] = []
                all_reqs = driver.find_element(By.XPATH, req_path)
                req_ind = all_reqs.find_elements(By.XPATH, "./child::*")
                j = 1
                while j < len(req_ind):
                    current_req = req_ind[j].get_attribute("title")
                    class_reqs[course_code].append(current_req)
                    j += 1
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


class_reqs = addReqs(programs)
toCSV('output2.csv', class_reqs)

driver.quit()