#!/usr/bin/python
import pandas as pd
import os
import datetime as dt

# file format constants
SEP = ','
ENCODING = 'utf-8'

# data has 25 rows of meta-data in every file
SKIP_ROWS = 25

# in/out file paths
RAW_DATA_DIR = os.path.join("./data/raw/")
OUT_DATA_DIR = os.path.join("./data/")
OUT_DATA_PATH = "daily_precip_data.csv"

# fields to keep in this dataset
COL_FILTER = ['Date/Time','Total Precip (mm)']

# weekday to day of week conversion
DAY_OF_WEEK = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# do transforms on dataset
def transform(df):
    # add day of week to dataset
    strpformat = '%Y-%m-%d'
    weekday = lambda date:dt.datetime.strptime(date, strpformat).weekday()
    dayofweek = lambda weekday:DAY_OF_WEEK[weekday]
    df.insert(1,'Day of Week', df['Date/Time'].apply(weekday).apply(dayofweek))

    # reset index so 0 - N
    df['index'] = range(0, len(df))
    df = df.set_index('index')
    
    return df

# append concatenated dataframe to another data frame
def append(df1, df2):
    return df1.append(df2)

# import csv file and return a dataframe
def importfile(filepath):
    df = pd.read_csv(filepath, skiprows=SKIP_ROWS, encoding=ENCODING, usecols=COL_FILTER)
    return df

# write dataframe to csv file
def writedf(df, filepath):
    df.to_csv(filepath, sep=SEP, encoding=ENCODING, header=True)

# setup function imports and transforms raw csv
# and saves as cleaned dataset in the ./data directory.
def main():
    finaldf = pd.DataFrame()
    for filename in os.listdir(RAW_DATA_DIR):
        if filename.endswith(".csv"):
            filepath = RAW_DATA_DIR + filename
            df = importfile(filepath)
            finaldf = append(finaldf, df)
    
    # clean up final data frame    
    finaldf = transform(finaldf)

    # export final datafile
    outfile = OUT_DATA_DIR + OUT_DATA_PATH
    writedf(finaldf, outfile)

main()