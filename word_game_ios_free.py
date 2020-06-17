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

browser.get('https://www.appannie.com/apps/ios/top-chart/?country=US&category=7019&device=iphone&date=2020-05-08&feed=Free&rank_sorting_type=rank&page_number=0&page_size=200&table_selections=&metrics=grossing_rank,category,all_avg,all_count,last_avg,last_count,first_release_date,last_updated_date,est_download,est_revenue,wau&order_type=desc&order_by=free_rank')

df = pd.DataFrame(columns=['App', 'Development Company', 'Free Rank', 'Grossing Rank','URL', 'Star Rating(after release)', 'Ratings(after release)', 'Star Rating(after update)', 'Ratings(after update)', 'Release Date', 'Last update date'])

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

        rate_after_release = cells[8].text
        rate = cells[10].text
        app_id = row.find_element_by_class_name('app-link').get_attribute('id')
        
        app = cells[1].text[:-1].split('\n')[0]
        development = cells[1].text[:-1].split('\n')[1]
        free_rank = cells[2].text
        grossing_rank = cells[4].text
        url = 'https://apps.apple.com/app/id{}'.format(app_id)
        star_rating_after_release = cells[7].text
        ratings_after_release = rate_after_release.replace(',','')
        star_rating = cells[9].text
        ratings = rate.replace(',','')
        release_date = cells[11].text
        last_update_date = cells[12].text
        
        ser = pd.Series([app, development, free_rank, grossing_rank,url, star_rating_after_release,ratings_after_release, star_rating, ratings, release_date, last_update_date], index = df.columns)
        df = df.append(ser, ignore_index=True)
        print('{} done'.format(len(df)))
    except:
        break
browser.quit()
df.to_excel('word_game_ios_free.xlsx')
