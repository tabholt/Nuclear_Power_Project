#############################################################################
# generate_load_factor_matrix.py
#
# load factors are only available through a separate part of the database
# and thus are only available on a separate sheet. The format of the excel
# file is highly inefficient given that it has over 8000 rows. Cleaning
# of the excel file is needed and then the 1-dimensional array form sheet
# is converted to a more efficient matrix layout.
#
# Input: load_factors.xlsx, reactors_complete.csv
# Output: load_factor_matrix.csv
#
# USED BY: initialize_database.py
#############################################################################

import numpy as np
import pandas as pd
import os

# import data sheets. reactors_complete is used as a reference for list
# of reactors over years. load_factors contains raw loadfactor data.
df = pd.read_csv('data/cleaned_data/reactors_complete.csv')
df_lf = pd.read_excel('data/virgin_data/load_factors/load_factors.xlsx',
                      headers=None, index_col=None)


# export and re-import load factors to remove merged cell anomalies
df_lf.to_csv('intermediate.csv', index=False)
df_lf = pd.read_csv('intermediate.csv')
os.remove('intermediate.csv')

# take only the columns we care about
df_lf = df_lf.iloc[:, [0, 1, 6, 11]]

# overwrite the column headers
df_lf.columns = ['plant', 'year', 'load_factor', 'data_completeness']

# delete rows that provided 'totals'
rows_to_delete = [0]
for i in range(df_lf.shape[0]):
    if (df_lf.iloc[i, 0] == df_lf.iloc[i, 1]):  # all 'total' rows shared this feature
        rows_to_delete.append(i)
    # delete strange anomaly plants
    if df_lf.loc[i, 'plant'] in ['Dimitrovgrad', 'TROITSK']:
        if i not in rows_to_delete:
            rows_to_delete.append(i)
df_lf = df_lf.drop(rows_to_delete)

# reset row indecies
df_lf = df_lf.reset_index(drop=True)

# find the unique plants and generate column of them
plant_list = []
for i in range(df.shape[0]):
    if not (df.loc[i, 'plant'] in plant_list):
        plant_list.append(df.loc[i, 'plant'])

# generate list of years where the loadfactor data is not available
year_list = np.linspace(1954, 1969, 1969-1953, dtype=int)

# create a matrix of NaN values that will be used to generate
# a template dataframe below
nan_matrix = np.empty((len(plant_list), len(year_list)))
nan_matrix[:] = np.nan


# create empty template data frame
matrix = pd.DataFrame(nan_matrix, columns=year_list, index=plant_list)

# populate dataframe with load factors
# populates the dataframe column at a time.
for i in range(df_lf.shape[0]):
    year = df_lf.loc[i, 'year']
    plant = df_lf.loc[i, 'plant']
    matrix.loc[plant, year] = df_lf.loc[i, 'load_factor']

# add on 2019 column for which we have no data yet.
matrix['2019'] = np.nan

# export cleaned sheet of load factors
matrix.to_csv('data/cleaned_data/load_factor_matrix.csv')
