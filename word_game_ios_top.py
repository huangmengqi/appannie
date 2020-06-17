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

browser.get('https://www.appannie.com/apps/ios/top-chart/?country=US&category=7019&device=iphone&date=2020-05-08&feed=Grossing&rank_sorting_type=rank&page_number=0&page_size=200&table_selections=&order_type=desc&order_by=paid_rank&metrics=free_rank,paid_rank,price,category,all_avg,all_count,last_avg,last_count,first_release_date,last_updated_date,est_download,est_revenue,wau')

df = pd.DataFrame(columns=['App', 'Development Company', 'Grossing Rank', 'Free Rank', 'Paid Rank', 'Price','URL', 'Star Rating(after release)', 'Ratings(after release)', 'Star Rating(after update)', 'Ratings(after update)', 'Release Date', 'Last update date'])

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
        app_id = row.find_element_by_class_name('app-link').get_attribute('id')
        rate_after_release = cells[11].text
        rate_after_update = cells[13].text
        
        app = cells[1].text[:-1].split('\n')[0]
        development = cells[1].text[:-1].split('\n')[1]
        grossing_rank = cells[2].text
        free_rank = cells[4].text
        paid_rank = cells[6].text
        price = cells[8].text
        url = 'https://apps.apple.com/app/id{}'.format(app_id)
        star_rating_after_release = cells[10].text
        ratings_after_release = rate_after_release.replace(',','')
        star_rating_after_update = cells[12].text
        ratings_after_update = rate_after_update.replace(',','')
        release_date = cells[14].text
        last_update_date = cells[15].text
        
        ser = pd.Series([app, development, grossing_rank, free_rank, paid_rank, price, url,star_rating_after_release, ratings_after_release, star_rating_after_update, ratings_after_update, release_date, last_update_date], index = df.columns)
        df = df.append(ser, ignore_index=True)
        print('{} done'.format(len(df)))
    except:
        break
browser.quit()
df.to_excel('word_game_ios_top.xlsx')
