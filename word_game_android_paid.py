# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 23:09:46 2020

@author: nouma
"""

from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.firefox.options import Options

options = Options()
browser = webdriver.Firefox(options= options)

browser.get('https://www.appannie.com/apps/google-play/top-chart/?country=US&category=40&device=&date=2020-05-08&feed=Paid&rank_sorting_type=rank&page_number=0&page_size=200&table_selections=&order_type=desc&order_by=paid_rank&metrics=grossing_rank,price,category,all_avg,all_count,first_release_date,last_updated_date,est_download,est_revenue,dau')

df = pd.DataFrame(columns=['App', 'Development Company', 'Paid Rank', 'Grossing Rank', 'Price', 'URL', 'Star Rating', 'Ratings', 'Release Date', 'Last update date'])

username = input('Enter your email address:')
password = input('Enter your password:')
while(True):
    try:
        browser.find_element_by_xpath("//input[@name='username']").send_keys(username)
        browser.find_element_by_xpath("//input[@type='password']").send_keys(password)
        browser.find_element_by_xpath("//button[@type='submit']").click()
        break
    except:
        continue
time.sleep(10)
rows = browser.find_elements_by_xpath("//tr[@class='main-row table-row']")
while(len(rows) == 0):
    time.sleep(10)
    rows = browser.find_elements_by_xpath("//tr[@class='main-row table-row']")
    time.sleep(1)
for row in rows:
    try:
        cells = row.find_elements_by_tag_name('td')

        str = row.find_element_by_tag_name('a').get_attribute('href')
        rate = cells[9].text
        
        app = cells[1].text[:-1].split('\n')[0]
        development = cells[1].text[:-1].split('\n')[1]
        free_rank = cells[2].text
        grossing_rank = cells[4].text
        price = cells[6].text
        url = 'https://play.google.com/store/apps/details?id='+str[46:].replace('/details/','')
        star_rating = cells[8].text
        ratings = rate.replace(',','')
        release_date = cells[10].text
        last_update_date = cells[11].text
        
        ser = pd.Series([app, development, free_rank, grossing_rank, price, url, star_rating, ratings, release_date, last_update_date], index = df.columns)
        df = df.append(ser, ignore_index=True)
        print('{} done'.format(len(df)))
    except:
        break
browser.quit()
df.to_excel('word_game_andoid_paid.xlsx')
