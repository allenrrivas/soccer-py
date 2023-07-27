import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from highlight_text import fig_text
from mplsoccer import VerticalPitch
import requests
from bs4 import BeautifulSoup
import json
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

shots = pd.DataFrame(data)

# Changing data type
shots['xG'] = shots['xG'].astype('float64')
shots['X'] = shots['X'].astype('float64')
shots['Y'] = shots['Y'].astype('float64')

shots['X1'] = (shots['X'])*100
shots['Y1'] = (shots['Y'])*100
# Original X and Y
shots['X'] = (shots['X'])*100
shots['Y'] = (shots['Y'])*100

# New dictionaries 
total_shots = shots[shots.columns[0]].count().tolist()
xGcum = np.round(max(np.cumsum(shots['xG'])),3).tolist()
xG_per_shot = np.round(max(np.cumsum(shots['xG']))/(shots[shots.columns[0]].count()),3).tolist()
goal = shots[shots['result']=='Goal']
shot_on_post = shots[shots['result']=='ShotOnPost']
saved_shot = shots[shots['result']=='SavedShot']
blocked_shot = shots[shots['result']=='BlockedShot']
missed_shot = shots[shots['result']=='MissedShots']
goals = goal[goal.columns[0]].count().tolist()

pitch = VerticalPitch(half=True, pitch_type='opta', pitch_color='#22312b', line_color='#ffffff', axis=True, label=True, tick=True)
fig, ax = pitch.draw(figsize=(12, 9))

plt.scatter(goal['Y'], goal['X'], s=(goal["xG"]* 720) + 100, c='#2ecc71', alpha=.7)
plt.scatter(shot_on_post['Y'], shot_on_post['X'], s=shot_on_post["xG"]* 720, c='#f1c40f', alpha=.7)
plt.scatter(saved_shot['Y'], saved_shot['X'], s=saved_shot["xG"]* 720, c='#3498db', alpha=.7)
plt.scatter(blocked_shot['Y'], blocked_shot['X'], s=blocked_shot["xG"]* 720, c='#9b59b6', alpha=.7)
plt.scatter(missed_shot['Y'], missed_shot['X'], s=(missed_shot["xG"]* 720), c='#e74c3c', alpha=.7)


s='<Vinícius Júnior Career Goals>'
highlight_textprops =[{"color": "#ffffff"}]
fig_text(s=s,
        x=0.27,y=0.4,
        highlight_textprops=highlight_textprops,
        fontname='monospace',
        fontsize=24
)

plt.show()