# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:19:17 2023

@author: kobas
"""


import pandas as pd
import os
import numpy as np
import datetime as dt
import pytz
import math


#%% Concat IAQ
# set the folder path
folder_path = '.\\IAQ'

# get all CSV files in the folder
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# create an empty dataframe to store the merged data
merged_df = pd.DataFrame()

# loop through the CSV files and append them to the merged dataframe
for file in csv_files:
    df = pd.read_csv(file, sep=';')  # specify the delimiter as ';'
    merged_df = pd.concat([merged_df, df])

merged_df["UNIX"] = merged_df['DateTime'].apply(lambda x: int(dt.datetime.timestamp(dt.datetime.strptime(x, '%d.%m.%Y %H:%M:%S'))))

# # write the merged dataframe to a CSV file
merged_df.to_excel('.\\04_IAQ.xlsx', index=False)


#%% Read all
df1 = pd.read_excel(".\\00_Meta.xlsx")
df2 = pd.read_excel(".\\00_Sessions.xlsx")
df3 = pd.read_excel(".\\01_Panas.xlsx")
df4 = pd.read_excel(".\\02_Comfort.xlsx")
df5 = pd.read_excel(".\\03_Attention.xlsx")
df6 = pd.read_excel(".\\04_IAQ.xlsx")
df7 = pd.read_csv(".\\05_AllEDACleanDown.csv")

#%% UNIX on Sessions (df2)
# Convert the datetime column to Unix timestamps
unix_timestamps1 = []
for ts in df2["Start"]:
    dt_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    dt_obj = dt.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    unix_timestamp = int(dt_obj.timestamp())
    unix_timestamps1.append(unix_timestamp)

df2["UNIX_Start"] = unix_timestamps1

unix_timestamps2 = []
for ts in df2["TestTime"]:
    dt_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    dt_obj = dt.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    unix_timestamp = int(dt_obj.timestamp())
    unix_timestamps2.append(unix_timestamp)

df2["UNIX_TestTime"] = unix_timestamps2

unix_timestamps3 = []
for ts in df2["End"]:
    dt_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    dt_obj = dt.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    unix_timestamp = int(dt_obj.timestamp())
    unix_timestamps3.append(unix_timestamp)

df2["UNIX_End"] = unix_timestamps3

df2.to_csv(".\\00_SessionsUNIX.csv")

#%% Tag session durations based on UNIX intervals on EDA (df7)# Load session data
sessions_df = df2

# Load UNIX data
unix_df = df7

# Create empty SessionID column
unix_df['SessionID'] = pd.NA

# Iterate over each session
for i, session in sessions_df.iterrows():
    
    # Get start and end times for session
    start_time = session['UNIX_Start']
    end_time = session['UNIX_End']
    
    # Get session ID
    session_id = session['SessionID']
    
    # Find UNIX values between start and end time for session
    session_unix = unix_df[(unix_df['UNIX'] >= start_time) & (unix_df['UNIX'] <= end_time)]
    
    # Set SessionID for UNIX values in session
    unix_df.loc[session_unix.index, 'SessionID'] = session_id

# Save updated UNIX data
unix_df.to_csv('.\\05_EDACleanDownSessions.csv', index=False)

# print(unix_df.iloc[1982,0])

#%% Tag session durations based on UNIX intervals on IAQ (df6)
# Load session data
sessions_df = df2

# Load UNIX data
unix_df = df6

# Create empty SessionID column
unix_df['SessionID'] = pd.NA

# Iterate over each session
for i, session in sessions_df.iterrows():
    
    # Get start and end times for session
    start_time = session['UNIX_Start']
    end_time = session['UNIX_End']
    
    # Get session ID
    session_id = session['SessionID']
    
    # Find UNIX values between start and end time for session
    session_unix = unix_df[(unix_df['UNIX'] >= start_time) & (unix_df['UNIX'] <= end_time)]
    
    # Set SessionID for UNIX values in session
    unix_df.loc[session_unix.index, 'SessionID'] = session_id

# Save updated UNIX data
unix_df.to_csv('.\\04_IAQ_SessID.csv', index=False)

# print(unix_df.iloc[1982,0])

#%% Time Elapsed
unix_df['Datetime'] = pd.to_datetime(unix_df['UNIX'], unit='s')
unix_df['Date'] = unix_df['Datetime'].dt.strftime("%Y-%m-%d")
unix_df['Time'] = unix_df['Datetime'].dt.strftime("%H:%M:%S")
unix_df['Time'] = pd.to_datetime(unix_df['Time'], errors='coerce')
unix_df.dtypes

grouped = unix_df.groupby('SessionID')

def time_elapsed(group):
    elapsed = group['Time'] - group['Time'].iloc[0]
    elapsed_minutes = elapsed.dt.total_seconds() / 60
    return elapsed_minutes

unix_df['ElapsedMinutes'] = grouped.apply(time_elapsed).reset_index(level=0, drop=True)

#%% Label first and last 10 mins
df0 = unix_df[unix_df["SessionID"].notnull()]

df0['StartEnd'] = 0
grouped = df0.groupby('SessionID')['Time'].agg(['first', 'last'])

for index, row in grouped.iterrows():
    session_start = row['first']
    session_end = row['last']
    df0.loc[(df0['SessionID'] == index) & (df0['Time'] <= session_start + pd.Timedelta(minutes=10)), 'StartEnd'] = 1
    df0.loc[(df0['SessionID'] == index) & (df0['Time'] >= session_end - pd.Timedelta(minutes=10)), 'StartEnd'] = 1

df0 = df0.reset_index()

#%% Merge 
dfIAQ = pd.read_csv(".\\04_IAQ_SessID.csv")
dfIAQ = dfIAQ[dfIAQ["SessionID"].notnull()]

df0['UNIX'] = df0['UNIX'].apply(lambda x: math.ceil(x))


merged1 = pd.merge_asof(df0.sort_values('UNIX'), dfIAQ.sort_values('UNIX'), on='UNIX', by='SessionID', direction='nearest')
merged1 = merged1.fillna(method='ffill')

merged1.to_csv('.\\10_MergedEDAIAQSessID.csv', index=False)


#%% Merge2: EDA, IAQ, Attention
# merge merged1 and df5
merged2 = pd.merge(merged1, df5, on='SessionID', how='outer')

# forward fill missing values
merged2 = merged2.ffill()


#%% Merge3: EDA, IAQ, Attention, Comfort
# merge merged2 and df4
merged3 = pd.merge(merged2, df4, on='SessionID', how='outer')

# forward fill missing values
merged3 = merged3.ffill()


#%% Merge4: EDA, IAQ, Attention, Comfort, Panas
# merge merged3 and df3
merged4 = pd.merge(merged3, df3, on='SessionID', how='outer')

# forward fill missing values
merged4 = merged4.ffill()

merged4.to_csv(".\\10_MergedAll.csv")