# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 17:31:50 2023

@author: kobas
"""

import heartpy as hp
import pandas as pd
import os
import glob
import pandas as pd
import heartpy as hp

#%% Reshape BVP csvs
# Define the path to search for CSV files
path = '.\\EMPATICA'

# Loop through all directories in the path
for dirpath, dirnames, filenames in os.walk(path):
    # Loop through all filenames in each directory
    for filename in filenames:
        # Check if the file is a CSV file and is named "EDA.csv"
        if filename == 'BVP.csv':
            # Get the full path to the CSV file
            filepath = os.path.join(dirpath, filename)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(filepath, header=None)

            # Get the value from the first row and first column of the DataFrame
            unix_val = df.iloc[0, 0]

            # Get the values from the "EDA" column, starting from the fourth row
            eda_val = df.iloc[3:, 0].reset_index(drop=True)
                
            # Combine the values into a new DataFrame
            new_df = pd.concat([pd.Series(unix_val), eda_val], axis=1)
            new_df.columns = ["UNIX", "BVP"]

            # Get the number of rows in the DataFrame
            num_rows = len(eda_val)

            # Loop through each row in the "UNIX" column, starting from the second row
            for i in range(1, num_rows):
                # Add 0.25 to the current value in the "UNIX" column
                new_df.loc[i, 'UNIX'] = new_df.loc[i-1, 'UNIX'] + 1/64
                
            # Get the new file path with the name "EDA2.csv"
            new_filepath = os.path.join(dirpath, 'BVP2b.csv')

            # Write the new DataFrame to the new file path
            new_df.to_csv(new_filepath, index=False)

#%% HRV features
# set the path to the directory containing the BVP2b.csv files
path = '.\EMPATICA'

# get a list of all BVP2b.csv files in the directory and its subdirectories
file_list = glob.glob(os.path.join(path, '**', 'BVP2b.csv'), recursive=True)

# loop over each file and extract HRV features
for file in file_list:
    # read in the data from the BVP2b.csv file
    df0 = pd.read_csv(file)

    # select the BVP data and convert it to a list
    bvp = df0['BVP'].tolist()

    # create a HeartPy signal object
    signal = hp.Signal(bvp, sample_rate=64)

    # process the signal to remove noise and artifacts
    filtered, _, _ = hp.filter_signal(signal.ppg, 
                                       cutoff = [0.8, 2.5], 
                                       sample_rate = signal.sample_rate, 
                                       order = 3, 
                                       filtertype='bandpass')

    # compute the heart rate and quality metrics
    working_data, measures = hp.process(filtered, sample_rate=signal.sample_rate)

    # compute HRV features
    hrv_features = hp.get_frequency_domain_features(measures['rr_list'])

    # create a new dataframe with the HRV features
    df1 = pd.DataFrame.from_dict(hrv_features, orient='index').T

    # set the output file path to BVP2clean.csv in the same directory as the input file
    output_file = os.path.join(os.path.dirname(file), 'BVP2clean.csv')

    # save the new dataframe to a CSV file
    df1.to_csv(output_file, index=False)

    # print the file path and HRV features
    print(file, hrv_features)