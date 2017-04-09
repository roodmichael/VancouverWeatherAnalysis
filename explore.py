# required libraries
import os
import calendar
import pandas as pd
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

# precipitation by year
df_year_sum = df.groupby(['year'], as_index=False)[['total_precip']].sum()

# pivot table
table = pd.pivot_table(df_year_sum, columns=['year'])
table.to_html(open(OUT_CHART_DIR + "total_precip_year.html", "w"))

# plot precipitation by year
p = ggplot(df_year_sum, aes(x="year", weight="total_precip")) +\
    geom_bar() +\
    xlab("Year") + ylab("Total Precipitation (mm)") +\
    theme_bw()
p.save(filename=OUT_CHART_DIR + "total_precip_year.png")

# sum precipitation by month
df_month_sum = df.groupby(['year','month'], as_index=False)[['total_precip']].sum()

# pivot table
table = pd.pivot_table(df_month_sum, columns=['month'], index=['year'])
table.to_html(open(OUT_CHART_DIR + "total_precip_month_year.html", "w"))

# plot precipitation per month per year
p = ggplot(df, aes(x="month", weight="total_precip")) +\
    facet_wrap("year") +\
    geom_bar() +\
    xlab("Month") + ylab("Total Precipitation (mm)") +\
    theme_bw()
filename = OUT_CHART_DIR + "total_precip_month_year.png"
p.save(filename=filename)

# average precipitation for month since 2000
df_month_mean = df_month_sum.groupby(['month'], as_index=False)[['total_precip']].mean()

# pivot table
table = pd.pivot_table(df_month_mean, columns=['month'])
table.to_html(open(OUT_CHART_DIR + "avg_precip_month.html", "w"))

# plot average precipitation per month since 2000
p = ggplot(df_month_mean, aes(x="month", weight="total_precip")) +\
    geom_bar(stat="mean") +\
    xlab("Month") + ylab("Avg. Precipitation (mm)") +\
    theme_bw()
filename = OUT_CHART_DIR + "avg_precip_month.png"
p.save(filename=filename)

# number of days with precipitation per year
df_year_count = df.groupby(['year'], as_index=False)[['any_precip']].sum()

# pivot table
table = pd.pivot_table(df_year_count, columns=['year'])
table.to_html(open(OUT_CHART_DIR + "numdays_precip_year.html", "w"))

# plot number of days with precipitation per year
p = ggplot(df_year_count, aes(x="year", weight="any_precip")) +\
    geom_bar() +\
    xlab("Year") + ylab("# Days with Precipitation") +\
    theme_bw()
filename = OUT_CHART_DIR + "numdays_precip_year.png"
p.save(filename=filename)

## ###############################
## Temperature Charts
## ###############################

# plot mean temp since 2010
p = ggplot(df, aes(x='date',y='mean_temp')) +\
    geom_line() +\
    xlab('Day') + ylab('Mean Temperature (C)')
p
filename = OUT_CHART_DIR + "mean_temp_daily_cont.png"
p.save(filename=filename)