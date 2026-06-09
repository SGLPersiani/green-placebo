# -*- coding: utf-8 -*-
"""
Created on Wed May  3 23:13:59 2023

@author: kobas
"""

import os
import pandas as pd
import numpy as np
import heartpy as hp

#%%Load data
# Load the raw PPG data from CSV
df = pd.read_csv('.//EMPATICA//1669794704_A03DBA_Nov 30//BVP2b.csv')

# Get the UNIX time column from the CSV
UNIX = df["UNIX"]

# Get the PPG data from the CSV
ppg = df["BVP"]

#%%HRV extraction
# Apply bandpass filter
filtered = hp.filter_signal(ppg, cutoff=[0.75, 3.5], sample_rate=64, order=3, filtertype='bandpass', return_top=True)

# Process the signal in segments
wd, m = hp.process_segmentwise(filtered, sample_rate=64.0, segment_width=240, segment_overlap=0.875, segment_min_size=0, calc_freq=True)

# Convert the HRV features to a DataFrame
measure = pd.DataFrame.from_dict(m)

#%%Clear outliers
measure2 = measure.copy()

# Clear the outliers for bpm, if they exist
measure2.loc[(measure2["bpm"] < 40 )|(measure2["bpm"] > 180 ), "bpm"] = np.NaN

# Clear the outliers for frequency domain features, if they exist
measure2.loc[((measure2["vlf"] > 10000)|(measure2["lf"] > 10000)|(measure2["hf"] > 20000)|(measure2["p_total"] > 40000)|(measure2["lf/hf"] > 5)), ('vlf',"lf",'hf','lf/hf','p_total','vlf_perc','lf_perc','hf_perc','lf_nu','hf_nu')] = np.NaN

#%%Format
measure2['segment_indices'] = measure2['segment_indices'].astype(str).str.strip('()')

# remove the parentheses
measure2['segment_indices'] = measure2['segment_indices'].str.strip('()')

# convert column to string data type
measure2['segment_indices'] = measure2['segment_indices'].astype(str)

# split the resulting string into two columns
measure2[['start', 'end']] = measure2['segment_indices'].str.split(',', expand=True)

# convert the start and end columns to integers
measure2['start'] = measure2['start'].astype(int)
measure2['end'] = measure2['end'].astype(int)

# create a new column UNIX_start and fill it with the corresponding UNIX value from the original CSV
measure2['UNIX'] = df.loc[measure2['start'], 'UNIX'].values

# remove the 'UNIX_start' column and save it in a separate variable
unix_start = measure2.pop('UNIX')

# insert the 'UNIX_start' column at the beginning of the DataFrame
measure2.insert(0, 'UNIX', unix_start)

#%%Save
# Save the updated HRV features to a CSV file
measure2.to_csv('.//EMPATICA//1669794704_A03DBA_Nov 30//HRV_features_updated.csv', index=False)

#%% Loop

# Set the path to the parent directory containing all the folders
path = 'EMPATICA'

# Loop through all the subdirectories in the parent directory
for root, dirs, files in os.walk(path):
    for file in files:
        # Check if the current file is a BVP2b.csv file
        if file.endswith('BVP2b.csv'):
            # Load the CSV file
            df = pd.read_csv(os.path.join(root, file))
            
            # Get the UNIX time column from the CSV
            UNIX = df["UNIX"]

            # Get the PPG data from the CSV
            ppg = df["BVP"]

            # Apply bandpass filter
            filtered = hp.filter_signal(ppg, cutoff=[0.75, 3.5], sample_rate=64, order=3, filtertype='bandpass', return_top=True)

            # Process the signal in segments
            wd, m = hp.process_segmentwise(filtered, sample_rate=64.0, segment_width=240, segment_overlap=0.875, segment_min_size=0, calc_freq=True)

            # Convert the HRV features to a DataFrame
            measure = pd.DataFrame.from_dict(m)

            measure2 = measure.copy()

            # Clear the outliers for bpm, if they exist
            measure2.loc[(measure2["bpm"] < 40 )|(measure2["bpm"] > 180 ), "bpm"] = np.NaN

            # Clear the outliers for frequency domain features, if they exist
            measure2.loc[((measure2["vlf"] > 10000)|(measure2["lf"] > 10000)|(measure2["hf"] > 20000)|(measure2["p_total"] > 40000)|(measure2["lf/hf"] > 5)), ('vlf',"lf",'hf','lf/hf','p_total','vlf_perc','lf_perc','hf_perc','lf_nu','hf_nu')] = np.NaN

            measure2['segment_indices'] = measure2['segment_indices'].astype(str).str.strip('()')

            # remove the parentheses
            measure2['segment_indices'] = measure2['segment_indices'].str.strip('()')

            # convert column to string data type
            measure2['segment_indices'] = measure2['segment_indices'].astype(str)

            # split the resulting string into two columns
            measure2[['start', 'end']] = measure2['segment_indices'].str.split(',', expand=True)

            # convert the start and end columns to integers
            measure2['start'] = measure2['start'].astype(int)
            measure2['end'] = measure2['end'].astype(int)

            # create a new column UNIX_start and fill it with the corresponding UNIX value from the original CSV
            measure2['UNIX'] = df.loc[measure2['start'], 'UNIX'].values

            # remove the 'UNIX_start' column and save it in a separate variable
            unix_start = measure2.pop('UNIX')

            # insert the 'UNIX_start' column at the beginning of the DataFrame
            measure2.insert(0, 'UNIX', unix_start)

            # Save the updated HRV features to a new CSV file
            output_filename = os.path.join(root, 'HRV_features_updated.csv')
            measure2.to_csv(output_filename, index=False)