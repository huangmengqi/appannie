from selenium import webdriver
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
browser = webdriver.Firefox()
browser.get('https://charts.youtube.com/charts/TopArtists/pt?hl=en')
#请求一个带有动态内容的网页，等待js执行完毕（10秒钟足够），获取当前浏览器render的内容的源码，关闭浏览器
time.sleep(10)
pageSource = browser.page_source
bsObj=BeautifulSoup(pageSource,"html.parser")
data = bsObj.find_all("ytmc-ellipsis-text",class_="ellipsis-title clickable style-scope ytmc-chart-table")

result = []
#with open('es.json', 'w') as fw:
for link in data:
    try:
        #artist name
        artistname = str(link.find("span", class_="ytmc-ellipsis-text style-scope"))
        artistnameend = (artistname.replace('<span class="ytmc-ellipsis-text style-scope">','')).replace('</span>','')
        #print(artistnameend)
        #loads:把json转换为dict
        s1 = json.loads(link['endpoint'])
        artistid = s1['browseEndpoint']['query']
        s2 = json.loads(artistid)
        urldata = (s2['entity_params_id']).replace('/','%2F')
        browser = webdriver.Firefox()
        browser.get('https://charts.youtube.com/artist/'+urldata+'?hl=en')
        time.sleep(10)
        pageSource = browser.page_source
        bsObj=BeautifulSoup(pageSource,"html.parser")
        #artist img
        artistimg = str(bsObj.find("img", class_="hero-img style-scope ytmc-hero"))
        artistimgend = (artistimg.replace('<img class="hero-img style-scope ytmc-hero" height="405" src="','')).replace('" width="720"/>','')
        #print(artistimgend)
        #total_plays
        total_plays = str(bsObj.find("h2", class_="views-card-views style-scope ytmc-views-card"))
        totalplaysend = (total_plays.replace('<h2 class="views-card-views style-scope ytmc-views-card">','')).replace('</h2>','')
        #print(totalplaysend)
        #exit()
        #data url
        dataurl = bsObj.find_all("paper-icon-button", class_="play-all style-scope ytmc-tracks-card")
        for link in dataurl:
            #artist img utl
            s1 = json.loads(link['endpoint'])
            artisturlend = s1['urlEndpoint']['url']
            temp_dict = {}
            temp_dict['name'] = artistnameend
            temp_dict['thumbnail'] = artistimgend
            temp_dict['total_plays'] = totalplaysend
            temp_dict['top_song'] = artisturlend
            result.append(temp_dict)
            print(artistnameend+'数据拉取完成！')
            browser.close()
        #json.dump(result,fw)
    finally:
        print(result)
        #json.dump(result,fw)
browser.close()
