#############################################################################
# initialize_database.py
#
# this program gets the database ready for use. The main functionality is
# essentially just calling the other programs that import and clean the data
# and then create a dictionary of data. This program has the added feature of
# displaying a nice loading animation and printing a time to run the cleaning
# functions. This program will not run the cleaning programs if the cleaned
# sheets already exist in their specified directories.
#
# USED BY: MAIN.py
#############################################################################

################################# IMPORTANT #################################
# IF YOU USE AN AUTO-PEP8 FORMATTER YOU MUST DISABLE ARGUMENT E402
# OTHERWISE THE AUTO-PEP WILL FUCK UP THIS PROGRAM!!!!!
# TO DISABLE ADD THE FOLLOWING TO YOUR SETTINGS.JSON FILE:
# "python.formatting.autopep8Args": ["--ignore=E402"]
#############################################################################

import itertools
import threading
import time
import sys


def animate():
    # this function simply prints the spinning loading animation
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r   computing... ' + c + '   ')
        sys.stdout.flush()
        time.sleep(0.125)
    sys.stdout.write('\r   Finished in    ')


#######################################################################
# Clean the reactor info sheets
#######################################################################
print('\n1. Interpreting and Cleaning Data\n')

# Check whether clean data exists in folder and if not, create it
try:
    fh = open('data/cleaned_data/reactors_complete.csv', 'r')
    hf = open('data/cleaned_data/carbon.csv', 'r')
    sd = open('data/cleaned_data/world_population.csv', 'r')
    print('   Data has been previously cleaned\n')
except:
    done = False
    then = time.time()  # Time before the operations start
    t = threading.Thread(target=animate)
    t.start()  # start the animation

    import clean_reactor_sheets
    import combine_reactor_sheets
    import clean_carbon_sheet
    import clean_population_data

    now = time.time()  # Time after it finished
    done = True  # stop the animation
    time.sleep(.3)  # pause required in case animation was in middle of a cycle
    print(round(now - then, 2), " seconds \n\n")  # print the time taken to run

#######################################################################
# Generate Database
#######################################################################

print('2. Generating Database\n')

done = False
then = time.time()  # Time before the operations start
t = threading.Thread(target=animate)
t.start()  # start animation

try:
    fh = open('data/cleaned_data/load_factor_matrix.csv', 'r')
except:
    import generate_load_factor_matrix

# The query_database_functions program runs the create_dictionary.py
# program which will be the final step to getting the database ready.
from query_database_functions import *


#######################################################################
# Add carbon data to the database
#######################################################################
# import the carbon sheet
df_carbon = pd.read_csv('data/cleaned_data/carbon.csv', index_col=0)

for i in range(1960, 2018):  # loop over years
    year = 'Year' + str(i)
    y = str(i)
    for j in range(len(Dict['Year1960'])):  # loop over plants
        # get country of current plant year
        country = Dict[year][j].get_country()
        # find that country's emissions that year in dataframe
        country_emissions = df_carbon.loc[country, y]
        Dict[year][j].set_country_emissions(
            country_emissions)  # write it to the database

now = time.time()  # Time after it finished
done = True
time.sleep(.3)
print(round(now - then, 2), " seconds \n\n")
