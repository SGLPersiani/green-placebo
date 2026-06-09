import os
import csv
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
import numpy as np


#%% Reshape EDA csvs
# Define the path to search for CSV files
path = '.\\EMPATICA'

# Loop through all directories in the path
for dirpath, dirnames, filenames in os.walk(path):
    # Loop through all filenames in each directory
    for filename in filenames:
        # Check if the file is a CSV file and is named "EDA.csv"
        if filename == 'EDA.csv':
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
            new_df.columns = ["UNIX", "EDA"]

            # Get the number of rows in the DataFrame
            num_rows = len(eda_val)

            # Loop through each row in the "UNIX" column, starting from the second row
            for i in range(1, num_rows):
                # Add 0.25 to the current value in the "UNIX" column
                new_df.loc[i, 'UNIX'] = new_df.loc[i-1, 'UNIX'] + 0.25
                
            # Get the new file path with the name "EDA2.csv"
            new_filepath = os.path.join(dirpath, 'EDA2b.csv')

            # Write the new DataFrame to the new file path
            new_df.to_csv(new_filepath, index=False)
            

#%% Get data and clean
# Loop through all subdirectories and files in the path
for subdir, dirs, files in os.walk(path):
    for file in files:
        # Check if the file is an EDA2b.csv file
        if file.endswith("EDA2b.csv"):
            # Load the CSV file
            filepath = os.path.join(subdir, file)
            df0 = pd.read_csv(filepath)
            eda_signal = df0["EDA"].values
            
            # Process the EDA signal
            signals, info = nk.eda_process(eda_signal, sampling_rate=8)
            cleaned = signals["EDA_Clean"]
            features = [info["SCR_Onsets"], info["SCR_Peaks"], info["SCR_Recovery"]]
            dfS = pd.DataFrame(signals)
            
            # Concatenate the original dataframe with the signals dataframe
            df_concat = pd.concat([df0, dfS], axis=1)
            
            # Save the concatenated dataframe to a CSV file
            csv_filename = os.path.join(subdir, "EDAClean.csv")
            df_concat.to_csv(csv_filename, index=False)
            
#%% Subject ID
# Loop through each folder
for folder_name in os.listdir(path):
    folder_path = os.path.join(path, folder_name)
    
    # Check if the folder contains an EDAClean.csv file
    if "EDAClean.csv" in os.listdir(folder_path):
        
        # Load the EDAClean.csv file
        df = pd.read_csv(os.path.join(folder_path, "EDAClean.csv"))
        
        # Add the folder name as a new column
        df["Folder"] = folder_name
        
        # Save the updated dataframe as EDAClean.csv in the same folder
        df.to_csv(os.path.join(folder_path, "EDAClean.csv"), index=False)

# Load the participant.csv file
participant_df = pd.read_excel(".\\00_FolderMatch.xlsx")

# Loop through each folder and read the EDAClean.csv file
for i, folder in enumerate(os.listdir(path)):
    # Get the full path to the EDAClean.csv file
    eda_file = os.path.join(path, folder, "EDAClean.csv")

    # Load the EDAClean.csv file
    eda_df = pd.read_csv(eda_file)

    # Merge the EDAClean.csv file with the participant_df on the "Folder" column
    merged_df = pd.merge(eda_df, participant_df, on="Folder", how="left")

    # Add the "Participant" column to the EDAClean.csv file
    eda_df["Participant"] = merged_df["Participant_y"]
    eda_df = eda_df.drop(['Folder'], axis=1)

    # Save the updated EDAClean.csv file
    eda_df.to_csv(eda_file, index=False)

#%% Minute means
path = '.\\EMPATICA'

# loop through each subfolder in the parent folder
for i, folder in enumerate(os.listdir(path)):
    
    # check if the current item in the parent folder is a directory
    if os.path.isdir(os.path.join(path, folder)):
        
        # set the path to the EDAClean.csv file in the current folder
        edaclean_path = os.path.join(path, folder, 'EDAClean.csv')
        
        # check if the EDAClean.csv file exists in the current folder
        if os.path.isfile(edaclean_path):
            
            # load the EDAClean.csv file as a dataframe
            edaclean = pd.read_csv(edaclean_path)
            
            # convert the UNIX column to a datetime object with seconds precision
            edaclean['datetime'] = pd.to_datetime(edaclean['UNIX'], unit='s')
            
            # set the datetime column as the index
            edaclean.set_index('datetime', inplace=True)
            
            # resample the dataframe to every minute and compute the mean
            edaclean_down = edaclean.resample('1T').mean()
            
            # fill any missing values with the previous value
            edaclean_down.fillna(method='ffill', inplace=True)
            
            # save the downsampled dataframe as a csv file in the same folder with the name EDACleanDown.csv
            edaclean_down.to_csv(os.path.join(path, folder, 'EDACleanDown.csv'), index=True, index_label='datetime')
            
            print(f"{i+1}. {folder}: EDACleanDown.csv saved.")
        
        else:
            print(f"{i+1}. {folder}: EDAClean.csv not found.")    

#%% Concat
# Create an empty list to store the dataframes
df_list = []

# Loop through all subdirectories and files in the path
for subdir, dirs, files in os.walk(path):
    for file in files:
        # Check if the file is an EDAClean.csv file
        if file == "EDACleanDown.csv":
            # Load the CSV file and append it to the list
            filepath = os.path.join(subdir, file)
            df = pd.read_csv(filepath)
            df_list.append(df)

# Concatenate all the dataframes into one
df_concat = pd.concat(df_list, axis=0)

# Save the concatenated dataframe to a CSV file
df_concat.to_csv(".\\05_AllEDACleanDown.csv", index=False)