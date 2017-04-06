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
RAW_DATA_ALT_DIR = os.path.join("./data/raw/alternate/")
OUT_DATA_DIR = os.path.join("./data/")
OUT_DATA_PATH = "daily_precip_data.csv"

# fields to keep in this dataset
COL_FILTER = ['Date/Time','Year','Month','Day','Total Precip (mm)']

# weekday to day of week conversion
DAY_OF_WEEK = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# do transforms on dataset
def transform(df):
    # rename columns
    df.columns = ["date","year","month","day","total_precip"]
    
    # add day of week to dataset
    strpformat = '%Y-%m-%d'
    weekday = lambda date:dt.datetime.strptime(date, strpformat).weekday()
    dayofweek = lambda weekday:DAY_OF_WEEK[weekday]
    df.insert(1,'dow', df['date'].apply(weekday).apply(dayofweek))

    # add binary has precipitation or not
    df['any_precip'] = df['total_precip'].apply(lambda x: 0 if(x<=0) else 1)
    
    # make date the index
    df = df.set_index('date')
    
    return df

# append concatenated dataframe to another data frame
def appenddf(df1, df2):
    return df1.append(df2)

# import csv file and return a dataframe
def importfile(filepath):
    df = pd.read_csv(filepath, skiprows=SKIP_ROWS, encoding=ENCODING, usecols=COL_FILTER)
    return df

# iterate over raw data files and import into data files
def importrawfiles(dir_path):
    df = pd.DataFrame()
    for filename in os.listdir(dir_path):
        if filename.endswith(".csv"):
            filepath = dir_path + filename
            currentdf = importfile(filepath)
            df = appenddf(df, currentdf)

    return df

# write dataframe to csv file
def writedf(df, filepath):
    df.to_csv(filepath, sep=SEP, encoding=ENCODING, header=True)

# impute missing cols from alternate data source 
def imputemissingdata(df, cols):
    # data frame from alternate sources
    altdf = importrawfiles(RAW_DATA_ALT_DIR)
    #altdf = transform(altdf)
    
    # break out of this and throw an error if the alternate data is not
    # the same length as the original dataframe.
    
    # look for missing precipitation data. replace with alternate data
    for col in cols:
        # file diagnostic - number of rows with missing precipitation data 
        # fill in missing data
        df[col].fillna(altdf[col], inplace=True)
        # file diagnostic - number of rows imputed.
        # file diagnostic - number of remains rows with missing values.
        # write file diagnostic

    # any further missing values assume no precipitation
    # need to decide on a better method of filling in remaining missing data
    df[col].fillna(0.0, inplace=True)

    return df 
    
# setup function imports and transforms raw csv
# and saves as cleaned dataset in the ./data directory.
def main():
    # import raw data files into data frame
    finaldf = importrawfiles(RAW_DATA_DIR)
    
    # replace missing values with data from nearby weather station
    finaldf = imputemissingdata(finaldf, ['Total Precip (mm)'])
    
    # clean up final data frame    
    finaldf = transform(finaldf)
    
    # export final datafile
    outfile = OUT_DATA_DIR + OUT_DATA_PATH
    writedf(finaldf, outfile)

main()