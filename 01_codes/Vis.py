# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:10:53 2023

@author: kobas
"""


import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import numpy as np
import re
import matplotlib.ticker as ticker
from matplotlib.font_manager import fontManager, FontProperties
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import zscore
from scipy.stats import ttest_ind



#%% Read
df = pd.read_csv(".\\10_MergedAllClean.csv")

# group the dataframe by SessionID and apply z-score normalization on EDA_Tonic column --> SessionID also grups by Participant, therefore normalisation per participant per session
df['EDA_Tonic_Z'] = df.groupby('SessionID')['EDA_Tonic'].transform(lambda x: zscore(x, ddof=1))
df['EDA_Phasic_Z'] = df.groupby('SessionID')['EDA_Phasic'].transform(lambda x: zscore(x, ddof=1))
df['EDA_Clean_Z'] = df.groupby('SessionID')['EDA_Clean'].transform(lambda x: zscore(x, ddof=1))
# These are single values per session, so normalised for participant
df['Error_Z'] = df.groupby('Participant')['ErrorsPerc'].transform(lambda x: zscore(x, ddof=1))
df['Total Comfort_Z'] = df.groupby('Participant')['Total score'].transform(lambda x: zscore(x, ddof=1))
df['AQ_Z'] = df.groupby('Participant')['Air quality'].transform(lambda x: zscore(x, ddof=1))
df['Atm_Z'] = df.groupby('Participant')['Atmosphere'].transform(lambda x: zscore(x, ddof=1))
df['Pos_Z'] = df.groupby('Participant')['Positive affect'].transform(lambda x: zscore(x, ddof=1))
df['Neg_Z'] = df.groupby('Participant')['Negative affect'].transform(lambda x: zscore(x, ddof=1))
#%% Fonts
path = "C:\\Users\\kobas\\Desktop\\Archivo_Condensed-Medium.ttf"
fontManager.addfont(path)
prop = FontProperties(fname=path)
sns.set(font=prop.get_name())


#%% EDAs per TEST 
fig, ax = plt.subplots(figsize=(15,12))
palette = sns.color_palette('Dark2', 8)

rc = {'axes.facecolor':'white',
      'axes.grid' : True,
      'grid.color': '.95',
      'font.size' : 16,
      "grid.linestyle" : "-"}
plt.rcParams.update(rc)
sns.despine()
ax.set_frame_on(False)

# order=["a", "b","c","d", "e", "f", "g", "h"]
order=[1,2,3,4]

sns.boxplot(x="Test", y="temperature", order=order, data=df, palette=palette)

# ax.axhline(y=0, color='black', linestyle='-', linewidth=0.75)

ax.set_ylabel("Temperature", fontsize=15, labelpad=10)
ax.set_xlabel('Test Scenarios', fontsize=15, labelpad=20)
#ax.set_title('Forest Plot of Mixed Effects Model: EDA vs Time of the Day', fontsize=12)
plt.xticks(fontsize=12, fontweight="bold")
plt.yticks(fontsize=12, fontweight="bold")
plt.show()


# group1 = df[df["Test"] == 4]["EDA_Clean_Z"]
# group2 = df[df["Test"] == 3]["EDA_Clean_Z"]
# p_value = ttest_ind(group1, group2).pvalue
# print(f"p-value between T1 and T2: {p_value:.3f}")

#%% Scatter


#%% Comfort per TEST