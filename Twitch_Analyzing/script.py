import codecademylib3_seaborn
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Bar Graph: Featured Games

games = ["LoL", "Dota 2", "CS:GO", "DayZ", "HOS", "Isaac", "Shows", "Hearth", "WoT", "Agar.io"]
viewers =  [1070, 472, 302, 239, 210, 171, 170, 90, 86, 71]

plt.figure(figsize=(12, 6))
plt.bar(range(len(games)), viewers, color='mediumslateblue')

# Labeling
plt.title("Featured Games on Twitch (Jan 1, 2015)")
plt.xlabel("Game")
plt.ylabel("Viewers")
plt.legend(["Viewers"], loc="upper right")
plt.xticks(range(len(games)), games, rotation=45)

plt.tight_layout()
plt.show()

# Pie Chart: League of Legends Viewers' Whereabouts

# Data
labels = ["US", "DE", "CA", "N/A", "GB", "TR", "BR", "DK", "PL", "BE", "NL", "Others"]
countries = [447, 66, 64, 49, 45, 28, 25, 20, 19, 17, 17, 279]
colors = ['lightskyblue', 'gold', 'lightcoral', 'gainsboro', 'royalblue', 'lightpink', 
          'darkseagreen', 'sienna', 'khaki', 'gold', 'violet', 'yellowgreen']
explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

# Pie chart
plt.figure(figsize=(10, 8))
plt.pie(countries,
        explode=explode,
        colors=colors,
        shadow=True,
        startangle=345,
        autopct='%1.0f%%',
        pctdistance=1.15)

# Add title and legend
plt.title("League of Legends Viewers' Whereabouts")
plt.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.show()


# Line Graph: Time Series Analysis

hour = range(24)

viewers_hour = [30, 17, 34, 29, 19, 14, 3, 2, 4, 9, 5, 48, 62, 58, 40, 51, 69, 55, 76, 81, 102, 120, 71, 63]

# Calculate error bounds (±15%)
y_upper = [v * 1.15 for v in viewers_hour]
y_lower = [v * 0.85 for v in viewers_hour]

# Line graph
plt.figure(figsize=(12, 6))
plt.plot(hour, viewers_hour, color='teal', label='Viewers per Hour')
plt.fill_between(hour, y_lower, y_upper, color='lightblue', alpha=0.2)

# Add labels and formatting
plt.title("US Viewers Over 24 Hours (Jan 1, 2015)")
plt.xlabel("Hour")
plt.ylabel("Viewers")
plt.xticks(range(24))
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

