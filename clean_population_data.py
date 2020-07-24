#############################################################################
# clean_population_data.py
# this program takes the population info excel sheet and transforms
# it into a form that is readable and easily manipulatable with python
#
# Input: world_population.xlsx
# Output: world_population.csv
#
#
# USED BY: initialize_database.py
#############################################################################

import pandas as pd
import numpy as np

# import datasets
df = pd.read_excel(
    'data/virgin_data/population/world_population.xlsx', index_col=None)
df_ref = pd.read_csv('data/cleaned_data/reactors_complete.csv')

# rename countries that have different name variations
for i in range(df.shape[0]):
    if df.loc[i, 'country'] == 'RUSSIAN FEDERATION':
        df.loc[i, 'country'] = 'RUSSIA'
    elif df.loc[i, 'country'] == 'CHINA, TAIWAN PROVINCE OF CHINA':
        df.loc[i, 'country'] = 'TAIWAN, CHINA'
    elif df.loc[i, 'country'] == 'REPUBLIC OF KOREA':
        df.loc[i, 'country'] = 'KOREA, REPUBLIC OF'
    elif df.loc[i, 'country'] == 'IRAN (ISLAMIC REPUBLIC OF)':
        df.loc[i, 'country'] = 'IRAN, ISLAMIC REPUBLIC OF'
    elif df.loc[i, 'country'] == 'CZECHIA':
        df.loc[i, 'country'] = 'CZECH REPUBLIC'

countries_ref = list(set(df_ref['country'].tolist()))
countries_ref.sort()

countries_pop = list(set(df['country'].tolist()))
countries_pop.sort()


to_delete = []
for i in range(df.shape[0]):
    if df.loc[i, 'country'] not in countries_ref:
        to_delete.append(i)

df = df.drop(to_delete)
df = df.reset_index(drop=True)


# verify we now have same set of countries
countries_carbon = list(set(df['country'].tolist()))
countries_carbon.sort()
for i in range(len(countries_carbon)):
    if (countries_carbon[i] != countries_ref[i]):
        print('DATA IS BAD')  # not printed when it runs so we know it's good!


df = df.round()
df = df.sort_values('country')

df.to_csv('data/cleaned_data/world_population.csv', index=False)
