import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time

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


edited_programs = degree_programs
i = 0
while i < len(edited_programs):
    edited_programs[i] = edited_programs[i].lower().replace(" ", "-")
    edited_programs[i] = edited_programs[i].replace(",", "")
    edited_programs[i] = edited_programs[i].replace(".", "")
    i += 1


driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)
link = driver.find_element(By.LINK_TEXT("Aerospace Studies Minor"))
link.click()