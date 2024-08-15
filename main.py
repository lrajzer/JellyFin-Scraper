from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from secret import USERNAME, PASSWORD
from time import sleep
import json
import re

url = 'http://192.168.55.20:30013/web/#/movies.html?topParentId=f137a2dd21bbc1b99aa5c0f6bf02a805'

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(3)

button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/div[2]/button[1]')
button.click()
driver.implicitly_wait(2)

login_box = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/form/div[2]/input')
pass_box = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/form/div[3]/input')
driver.implicitly_wait(1)
login_box.send_keys(USERNAME)
pass_box.send_keys(PASSWORD)
login_button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/form/button')
driver.implicitly_wait(1)
login_button.click()

driver.implicitly_wait(3)


movies_dict = {
}
season_dict = {
}

season_regex = re.compile(r'[eE][0-9]{1,}')

for j in range(1, 53):
    print(f"********************** Page {j} started **********************")
    
    for i in range(1, 101):
        elements = driver.find_element(by=By.XPATH, value=f'/html/body/div[1]/div[4]/div[2]/div[1]/div[3]/div[{i}]')
        name = None
        if len(elements.text.split('\n')) == 2:
            name = elements.text.split('\n')[0]
        else:
            name = elements.text.split('\n')[1]
        if season_regex.search(name):
            print(f'{name} is a season of TV')
            season_dict[name] = 1
        if name not in movies_dict:
            movies_dict[name] = 1
            # print(f'{name} is added')
        else:
            movies_dict[name] += 1
            print(f'{name} is duplicated')
    driver.implicitly_wait(1)
    print(f"********************** Page {j} finished **********************")
    print(movies_dict)
    next_button = driver.find_element(by=By.XPATH, value=f'/html/body/div[1]/div[4]/div[2]/div[1]/div[4]/div/div/div/button[2]')
    next_button.click()
    print(f"********************** Page {j+1} clicked **********************")
    with open('movies.json', 'w') as f:
        json.dump(movies_dict, f)
    with open('movies_duplicate.json', 'w') as f:
        duplicate_dict = {k: v for k, v in movies_dict.items() if v > 1}
        json.dump(duplicate_dict, f)
    with open('seasons.json', 'w') as f:
        json.dump(season_dict, f)
    sleep(4)

for key in movies_dict:
    if movies_dict[key] > 1:
        print(f'{key} is duplicated {movies_dict[key]} times')



# input()