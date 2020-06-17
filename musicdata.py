


import requests
import json

url = 'https://charts.youtube.com/youtubei/v1/browse?alt=json&key=AIzaSyCzEW7JUJdSql0-2V4tHUb6laYm4iAE_dM'
wbdata = requests.get(url).text

print(wbdata)
