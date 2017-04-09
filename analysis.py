# required libraries
import os
import datetime
import pandas as pd
import numpy as np
from ggplot import *

# file format constants
SEP = ','
ENCODING = 'utf-8'
    
# in/out file paths
OUT_DATA_DIR = os.path.join("./data/")
OUT_DATA_FILE = "daily_precip_data.csv"
OUT_DATA_PATH = OUT_DATA_DIR + OUT_DATA_FILE
OUT_CHART_DIR = os.path.join("./charts/")

# import cleaned data file 
df = pd.read_csv(OUT_DATA_PATH, encoding=ENCODING)
df['index'] = df['date']
df = df.set_index('index')
df['date'] =  pd.to_datetime(df['date'], format='%Y-%m-%d')

## ########################
## Analysis
## ########################

## ########################
## 1. How many days per year can I comfortably lay on the beach? (number of days above temp XX and not raining)
df_grouped = pd.DataFrame()
groups = []
for temp in range(22, 32, 2):
    new_column = 'is_beach_weather_' + str(temp)
    df['num_days'] = 0
    df['num_days'][(df['max_temp'] >= temp) & (df['any_precip'] == 0)] = 1

    df_tmp = df.groupby(['year'], as_index=False)[['num_days']].sum()
    df_tmp['group'] = '> ' + str(temp) + '(C)'
    groups.append(df_tmp)

# create grouped dataset by temperature
df_grouped = pd.concat(groups)

# pivot table
table = pd.pivot_table(df_grouped, values='num_days', columns=['year'], index=['group'])
table['average_days'] = table.mean(axis=1)
table.to_html(open(OUT_CHART_DIR + "num_days_beach_weather.html", "w"))

# plot
p = ggplot(df_grouped, aes(x='group', y='num_days')) +\
    geom_boxplot() +\
    xlab("Temperature (Min)") + ylab("Number of days")
p.save(filename=OUT_CHART_DIR + "num_days_beach_weather.png")

## ##########################
## 2. How many days per year do I need to carry an umbrella? (number of days rains more than XX)
df_grouped = df.groupby(['year'], as_index=False)[['any_precip']].sum()

# pivot table
table = pd.pivot_table(df_grouped, columns=['year'])
table['avg_days'] = table.mean(axis=1)
table.to_html(open(OUT_CHART_DIR + "num_days_need_umbrella.html", "w"))

# plot precipitation by year
p = ggplot(df_grouped, aes(x="year", weight="any_precip")) +\
    geom_bar() +\
    xlab("Year") + ylab("Number of rainy days")
p.save(filename=OUT_CHART_DIR + "num_days_need_umbrella.png")

# 3. How many bottles of sunscreen will a Korean woman need per year in Vancouver (how many days per year and how many mills of sunscreen in a bottle)
# Trick question. 365.

# 4. How many bbqs can I have per year (assuming max 1 per day) (not raining and above XX)
df['can_bbq'] = 0
df['can_bbq'][(df['max_temp'] >= 15) & (df['any_precip'] == 0)] = 1
df_grouped = df.groupby(['year'], as_index=False)[['can_bbq']].sum()

# pivot table
table = pd.pivot_table(df_grouped, columns=['year'])
table['avg_days'] = table.mean(axis=1)
table.to_html(open(OUT_CHART_DIR + "num_days_can_bbq.html", "w"))

# plot precipitation by year
p = ggplot(df_grouped, aes(x="year", weight="can_bbq")) +\
    geom_bar() +\
    xlab("Year") + ylab("Number of bbq days")
p.save(filename=OUT_CHART_DIR + "num_days_can_bbq.png")

# 5. How many bbq weekends do we get per year (weekend, 1 day not raining, above XX)
df_filtered = df[['year','week_num','can_bbq']][(df.is_weekend == 1)]
df_grouped = df_filtered.groupby(['year','week_num'], as_index=False).max()
df_grouped = df_grouped[['year','can_bbq']].groupby(['year'], as_index=False).sum()

# pivot table
table = pd.pivot_table(df_grouped, columns=['year'])
table['avg_days'] = table.mean(axis=1)
table.to_html(open(OUT_CHART_DIR + "num_weekends_can_bbq.html", "w"))

# plot bbq weekends by year
p = ggplot(df_grouped, aes(x="year", weight="can_bbq")) +\
    geom_bar() +\
    xlab("Year") + ylab("Number of bbq weekends")
p.save(filename=OUT_CHART_DIR + "num_weekends_can_bbq.png")

# 6. Number of days per year I need an AC unit (where min temperature above XX)
# 7. When will my tomatoes ripen.
#      Assume you plant on memorial day and you need X days of sunlight to ripen
# 8. How many days per year can I camp in Vancouver (above temperature XX and not raining above YY)