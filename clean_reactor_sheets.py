#############################################################################
# clean_reactor_sheets.py
# this program takes the 4 different reactor info excel sheets and transforms
# them into a form that is readable and easily manipulatable with python
#
# Input: reactors1.xlsx, reactors2.xlsx, reactors3.xlsx, reactors4.xlsx
# Output: reactors1_clean.csv, reactors2_clean.csv, reactors3_clean.csv,
#         reactors4_clean.csv
#
#
# USED BY: initialize_database.py
#############################################################################

import pandas as pd
import numpy as np


def clean_spreadsheet(sheet_name, read_directory, write_directory):

    df = pd.read_excel(
        read_directory + sheet_name + '.xlsx', header=None)

    # import the list of countries from excel file that is a mess
    countries = pd.read_excel(read_directory + 'countries.xlsx', header=None)
    countries = countries[0].tolist()  # change dataframe to list
    countries = set(countries)  # eliminate duplicate entries from list

    # delete any mysterious columns of NaN
    df = df.dropna(axis='columns', thresh=5)

    # loop over the columns of the matrix and replace the NaN values that resulted
    # from merged cells with the years
    for i in range(df.shape[1]):
        if (pd.isna(df.iloc[0, i]) and i > 1):
            df.iloc[0, i] = df.iloc[0, i-1]

    # put country names in first column
    for i in range(df.shape[0]):
        if not(df.iloc[i, 0] in countries):
            if not(pd.isna(df.iloc[i, 0])):  # ignore first couple rows which are NaN
                # the row above will always contain country name
                df.iloc[i, 0] = df.iloc[i-1, 0]

    # delete the rows that contain country summary statistics
    to_delete = []
    for i in range(df.shape[0]):
        if (pd.isna(df.iloc[i, 1]) and i >= 1):
            to_delete.append(i)
    df = df.drop(to_delete)

    # write in column headers for the first two headers
    df.iloc[0, 0] = 'country'
    df.iloc[0, 1] = 'plant'

    # write the clean files to the write_directory
    df.to_csv(write_directory + sheet_name + '_clean' +
              '.csv', header=False, index=False)


# call the function 4 times to clean the 4 sheets
for i in range(4):
    clean_spreadsheet('reactors%d' % (
        i+1), 'data/virgin_data/reactors_capacity/', 'data/cleaned_data/')
