import matplotlib.pyplot as plt
from matplotlib.patheffects import withSimplePatchShadow
import numpy as np
import pandas as pd
import mplcursors
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

# shots['X1'] = (shots['X'])*100
# shots['Y1'] = (shots['Y'])*100
# Original X and Y
shots['X'] = (shots['X'])*100
shots['Y'] = (shots['Y'])*100

# New dictionaries 
total_shots = shots[shots.columns[0]].count().tolist()
xGcumsum = np.round(max(np.cumsum(shots['xG'])),3).tolist()
xG_per_shot = np.round(max(np.cumsum(shots['xG']))/(shots[shots.columns[0]].count()),3).tolist()
goal = shots[shots['result']=='Goal']
shot_on_post = shots[shots['result']=='ShotOnPost']
saved_shot = shots[shots['result']=='SavedShot']
blocked_shot = shots[shots['result']=='BlockedShot']
missed_shot = shots[shots['result']=='MissedShots']
# Count Number of Goals
goals = goal[goal.columns[0]].count().tolist()

pitch = VerticalPitch(half=True, pitch_type='opta', pitch_color='#22312b', line_color='#ffffff', axis=False)
fig, ax = pitch.draw(figsize=(12, 9))

# goal_x = plt.scatter(goal['Y'], goal['X'], s=(goal["xG"]* 720) + 100, c='#2ecc71', label='Goals', alpha=.7)
# shot_on_post_x = plt.scatter(shot_on_post['Y'], shot_on_post['X'], s=shot_on_post["xG"]* 720, c='#f1c40f', label='Shots On Post', alpha=.7)
# saved_shot_x = plt.scatter(saved_shot['Y'], saved_shot['X'], s=saved_shot["xG"]* 720, c='#3498db', label='Saved Shots', alpha=.7)
# blocked_shot_x = plt.scatter(blocked_shot['Y'], blocked_shot['X'], s=blocked_shot["xG"]* 720, c='#9b59b6', label='Blocked Shots', alpha=.7)
# missed_shot_x = plt.scatter(missed_shot['Y'], missed_shot['X'], s=(missed_shot["xG"]* 720), c='#e74c3c', label='Missed Shots', alpha=.7)


plt.scatter(shots['Y'], shots['X'], s=shots['xG']*720, c='#e74c3c', alpha=0.7)


# legend = ax.legend(loc="upper center", bbox_to_anchor= (0.14, 0.88), labelspacing=0.9, prop={'weight':'bold', 'size':11})
# legend.legendHandles[0]._sizes = [300]
# legend.legendHandles[1]._sizes = [300]
# legend.legendHandles[2]._sizes = [300]
# legend.legendHandles[3]._sizes = [300]
# legend.legendHandles[4]._sizes = [300]

bbox_pad = 2
bboxprops = {'linewidth': 0, 'pad': bbox_pad}

s='<Vinícius Júnior Career Shots>'
highlight_textprops =[{'color': '#ffffff', 'weight': 'bold', 'bbox': {'facecolor':'#22312b', **bboxprops}}]
fig_text(s=s,
        x=0.27,y=0.15,
        highlight_textprops=highlight_textprops,
        fontname='monospace',
        fontsize=24
)

fig_text(x=0.42, y=0.37, s="Shots:\n\nxGcumsum:\n\nxG per shot:\n\nGoals: ", fontsize = 12, fontweight = "bold", c='#ffffff')
fig_text(x=0.52, y=0.37, s="<{}\n\n{}\n\n{}\n\n{}>".format(total_shots,xGcumsum,xG_per_shot,goals), fontsize = 12, fontweight = "bold", c='#2ecc71')


# print(goal)

# Hover Annotations
def show_hover_panel(get_text_func=None):
    cursor = mplcursors.cursor(
        hover=2,  # Transient
        annotation_kwargs=dict(
            bbox=dict(
                boxstyle="square,pad=0.5",
                facecolor="white",
                edgecolor="#ddd",
                linewidth=0.5,
                path_effects=[withSimplePatchShadow(offset=(1.5, -1.5))],
            ),
            linespacing=1.5,
            arrowprops=None,
        ),
        highlight=True,
        highlight_kwargs=dict(linewidth=2),
    )

    if get_text_func:
        cursor.connect(
            event="add",
            func=lambda sel: sel.annotation.set_text(get_text_func(sel.index)),
        )
        
    return cursor


def on_add(index):
        
#     goal_i = goal.iloc[index]
#     shot_on_post_i = shot_on_post.iloc[index]
#     saved_shot_i = saved_shot.iloc[index]
#     blocked_shot_i = blocked_shot.iloc[index]
#     missed_shot_i = missed_shot.iloc[index]
#     items = [goal_i, shot_on_post_i, saved_shot_i, blocked_shot_i, missed_shot_i]
#     for item in items:
#         parts = [
#                 f"xG: {item.xG}",
#                 f"Minute: {item.minute}",
#                 f"Situation: {item.situation}"
#         ]

        item = shots.iloc[index]
        parts = [
                f"xG: {item.xG:,.2f}",
                f"Minute: {item.minute}",
                f"Situation: {item.situation}"
        ]


        return "\n".join(parts)

show_hover_panel(on_add)

plt.show()