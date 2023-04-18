import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time
import csv

def scrapeClasses():
    try:
        requirements = driver.find_element(By.PARTIAL_LINK_TEXT, "REQUIREMENTS")
        requirements.click()
        source = driver.page_source
        soup2 = BeautifulSoup(source, "html.parser")
        classes = soup2.find("table", class_ = "sc_courselist")
        classes_list = classes.find_all("td", class_ = "codecol")
        for classes in classes_list:
            print(classes.text)
        driver.get(url)
    except:
        driver.get(url)


def addCourses(programs):
    majors_classes = {}
    for program in degree_programs:
        if 'major' in program.lower():
            courses = []

            if program.find("Biomedical") != -1: ## Edge case - BME
                link = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[2]/div/ul[2]/li[5]/a')
            else:
                link = driver.find_element(By.PARTIAL_LINK_TEXT, program)

            link.click()

            requirements = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/nav/ul/li[3]/a')
            requirements.click()
            source = driver.page_source
            soup2 = BeautifulSoup(source, "html.parser")
            classes = soup2.find("table", class_ = "sc_courselist")
            classes_list = classes.find_all("td", class_ = "codecol")
            for course in classes_list:
                course_code = course.text
                course_code = course_code.replace("\xa0", " ")
                courses.append(course_code)
            majors_classes[program] = courses
            
            driver.get(url)
    return majors_classes


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



url = "https://catalog.unc.edu/undergraduate/programs-study/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
total = soup.find("div", class_ = "az_sitemap")
headings = total.find_all("li")

degree_programs = []
degree_raw = []
count = 0
for heading in headings:
    program = heading.text
    if len(program) > 2:
        degree_programs.append(heading.text)
        degree_raw.append(heading)


driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)
classes = addCourses(degree_programs)
toCSV('output.csv', classes)

driver.quit()