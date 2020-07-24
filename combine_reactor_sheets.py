#############################################################################
# combine_reactor_sheets.py
# this program stitches the 4 different reactor info sheets into a single
# dataframe that improves efficiency and simplicty of data analysis process.
# This is the most computationally intense program in the project, taking
# approximately 10s to run on laptop.
#
# Input: reactors1_clean.csv, reactors2_clean.csv, reactors3_clean.csv,
#        reactors4_clean.csv
# Output: reactors_complete.csv
#
#
# USED BY: initialize_database.py
#############################################################################

import os
import numpy as np
import pandas as pd


# define function that will combine dataframes

def combine_dataframes(df, df_s):
    # the input df can be thought of as a master dataframe
    # the input df_s is the secondary dataframe
    # values are read and interpreted from the secondary dataframe
    # and then written to the appropriate cell in the master dataframe
    for i in range(df_s.shape[0]):  # iterate over rows of secondary dataframe
        found_match = False
        k = 0
        # find index of first zero-row avoids looping unnecessarily
        while df.iloc[k, 0] != 0:
            k += 1
        # iterate over non-zero rows of main dataframe looking for matching plants
        # this is how we see if plant has previously been written to master dataframe
        for j in range(k):
            if (df.loc[j, 'plant'] == df_s.loc[i, 'plant']):
                found_match = True
                break  # improves code efficiency
        # iterate over each column of the secondary dataframe
        for header in list(df_s.columns):
            if not pd.isna(df_s.loc[i, header]):  # ignore NaN cols
                # if the plant already exists in main dataframe
                if found_match:
                    # copy cell from small dataframe to main dataframe
                    df.loc[j, header] = df_s.loc[i, header]
                else:
                    # create new row if plant didnt already exist in main dataframe
                    df.loc[k, header] = df_s.loc[i, header]
    return df


# import the cleaned data sheets
df1 = pd.read_csv('data/cleaned_data/reactors1_clean.csv')
df2 = pd.read_csv('data/cleaned_data/reactors2_clean.csv')
df3 = pd.read_csv('data/cleaned_data/reactors3_clean.csv')
df4 = pd.read_csv('data/cleaned_data/reactors4_clean.csv')

# create a list of column headers that countains all they years
col_headers = ['country', 'plant']
for i in range(1954, 2020):
    col_headers.append(str(i))
    col_headers.append(str(i) + '.0')

# create a dataframe that is full of zeros
# dataframe must have enough rows to acomodate data
max_rows = df1.shape[0] + df2.shape[0] + df3.shape[0] + df4.shape[0]
zeros = np.zeros((max_rows, len(col_headers)), dtype=int)
df = pd.DataFrame(zeros, columns=col_headers)

# write the small subdataframe to the master dataframe one at a time
df = combine_dataframes(df, df1)
df = combine_dataframes(df, df2)
df = combine_dataframes(df, df3)
df = combine_dataframes(df, df4)

# determine how many non-zero rows there are
i = 0
while df.iloc[i, 0] != 0:
    i += 1
# keep only non-zero rows
df = df.head(i)

# order alphabetically be country then reactor
df = df.sort_values(['country', 'plant'])

# delete temp sheets
os.remove('data/cleaned_data/reactors1_clean.csv')
os.remove('data/cleaned_data/reactors2_clean.csv')
os.remove('data/cleaned_data/reactors3_clean.csv')
os.remove('data/cleaned_data/reactors4_clean.csv')

# export reactors complete sheet
df.to_csv('data/cleaned_data/reactors_complete.csv', index=False)
