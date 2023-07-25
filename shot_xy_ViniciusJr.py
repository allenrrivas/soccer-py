import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

link = "https://understat.com/player/7008"
res = requests.get(link)
soup = BeautifulSoup(res.content,'lxml')
scripts = soup.find_all('script')
# Get the grouped stats data, it's the second script executed in order
strings = scripts[3].string
# Getting rid of unnecessary characters from json data
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')
data = json.loads(json_data)

df = pd.DataFrame(data)
df.to_csv('shot_xy_ViniciusJr.csv', sep='\t', encoding='utf-8')
print(df)