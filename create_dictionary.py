#############################################################################
# create_dictionary.py
#
# reads all information interpreted from the downloaded excel sheets and
# enters it into a class, "Plantyear" which contains all relivant info
# for the plant in the given year. Instances of Plantyear are stored in a
# dictionary that is indexed by year for efficient and easy access to all
# class atributes.
#
# Input: reactors_complete.csv, load_factor_matrix.csv
# Output: Dict (dictionary of Plantyears)
#############################################################################


import pandas as pd
import numpy as np
from plant_Class import *


################################################################################
#
# DECIDE TREATMENT FOR N/A LOAD FACTORS
# 0 will set load factors to zero for missing data
# 1 will set them to lowest loadfactor of available years
# 2 will set them to average of all years

treatment = 2

################################################################################


def extract_plant_year(df, year, row):
    year = str(year)
    plant_year = []
    country = df.iloc[row, 0]
    name = df.iloc[row, 1]
    num_reactors = df.loc[row, year]
    if (pd.isna(df.loc[row, year + '.0'])):
        df.loc[row, year + '.0'] = 0
    if (pd.isna(df.loc[row, year])):
        df.loc[row, year] = 0
    capacity = int(df.loc[row, year + '.0'])
    year = int(year)
    plant_year.append(name)
    plant_year.append(country)
    plant_year.append(year)
    plant_year.append(num_reactors)
    plant_year.append(capacity)
    return plant_year


df = pd.read_csv('data/cleaned_data/reactors_complete.csv')
df_lf = pd.read_csv('data/cleaned_data/load_factor_matrix.csv', index_col=0)

# calculate na loadfactor based on selection


def calc_na_lf(df, treatment, plant):
    if treatment == 0:
        na_lf = 0
    elif treatment == 1:
        if np.isnan(df.loc[plant, :]).all():
            na_lf = 0
        else:
            na_lf = np.nanmin(df.loc[plant, :])
    else:
        if np.isnan(df.loc[plant, :]).all():
            na_lf = 0
        else:
            na_lf = np.nanmean(df.loc[plant, :])
    return na_lf


# Creates an array of plants per year ordered per plants
plant_array = []
for j in range(df.shape[0]):  # iterate over plants
    plant = df.loc[j, 'plant']
    load_factor_nan = calc_na_lf(df_lf, treatment, plant)
    for i in range(int((df.shape[1] - 2) / 2)):
        year = 1954 + i
        extraction = extract_plant_year(df, year, j)
        year = str(year)
        if df_lf.loc[plant, year] > 0:
            load_factor = df_lf.loc[plant, year]
        else:
            load_factor = load_factor_nan
        if extraction[-1] == 0:  # if plant has no capacity make load factor zero
            load_factor = 0
        extraction.append(load_factor)
        plant_array.append(extraction)


# Resort plant_array to be a list of plants ordered per year
# example: atucha 1954,embalse 1954..

# this sort is necessary because loop was oposite order
# of dictionary. We do this to reduce the calc_na_lf()
# function calls by factor of 66.

# # take second element for sort
def takeSecond(plant_array):
    return plant_array[2]


plant_array.sort(key=takeSecond)
# print(plant_array)


# Creates a list with one row and many columns containing Plantyear
# = plant objects with specifics and iterates over years
# 1 plant with all the years than the other plant with all the years etc..
PlantyearList = []
for i in range(len(plant_array)):
    PlantyearList.append(Plantyear(
        plant_array[i][0], plant_array[i][1], plant_array[i][2], plant_array[i][3], plant_array[i][4], plant_array[i][5]))


# Creates a dictionnary with years as keys and with elements being the objects
# (reactors) in each respective year
Dict = {}

for x in range(int((df.shape[1] - 2) / 2)):
    m = df.shape[0]
    for j in range(m):
        Dict['Year' + str(x + 1954)] = PlantyearList[(x * m):(x * m) + j + 1]
