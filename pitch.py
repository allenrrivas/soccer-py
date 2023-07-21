from mplsoccer import Pitch
import matplotlib.pyplot as plt

pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
fig, ax = pitch.draw()
plt.show()