#############################################################################
# query_database_functions.py
#
# contains all of the helper functions that are used to pull and treat
# usefull infromation from the database. Also contains dictionaries that
# are used to put labels on the plots of the information. These functions
# are extensively called in the MAIN.py program.
#
# USED BY: initialize_database.py, MAIN.py
#############################################################################


import numpy as np
from matplotlib import pyplot as plt
from create_dictionary import *
from reference_stats import *

# if plots are coming out fuzzy un-comment this line
# plt.rcParams['figure.dpi'] = 150


statistic_dict = {
    # Labels for Statistics
    1: 'Actual Power Output (TWh)',
    2: 'Available Capacity (MW)',
    3: 'Number of Reactors',
    4: 'Load Factors (%)',
    5: 'Number of Plants',
    6: 'CO2 Emissions (Metric Mega Tonnes CO2)',
    # Labels for plot title
    11: 'Annual Nuclear Electricity Output',
    12: 'Annual Available Nuclear Power Capacity',
    13: 'Stock of Operational Reactors',
    14: 'Average Annual Load Factor',
    15: 'Stock of Operational Plants',
    16: 'Annual CO2 Emissions'
}


def ask_user_params():
    import itertools
    flag = True  # used to skip the input step if all years requested

    while True:
        ask = (
            input('Enter starting year between 1954 and 2019, or type "all" for all years:  '))
        try:
            start_year = int(ask)
            if ((start_year >= 1954) and (start_year <= 2019)):
                break
            else:
                print('date not in range')
        except:
            if ask == 'all':
                start_year = 1954
                end_year = 2018
                flag = False
                break
            else:
                print('invalid input')

    while flag:
        end_year = (input(
            "Enter ending year between 1954 and 2019 or enter number of years:  "))
        try:
            end_year = int(end_year)
            if (end_year + start_year - 1 <= 2019):
                end_year = end_year + start_year - 1
                break
            elif ((end_year >= start_year) and (end_year <= 2019)):
                break
            else:
                print('end date not in range')
        except:
            print('invalid input')
    print('\nyou have selected date range:   ',
          start_year, ' to ', end_year, '\n')

    # generate a list of countries that were active those years
    country_list = []
    for i in range(end_year - start_year):
        country_list.append(get_country_list(start_year + i))
    country_list = list(set(itertools.chain(*country_list)))
    country_list.sort()

    plant_list = []
    for i in range(end_year - start_year):
        plant_list.append(get_plant_list(start_year + i))
    plant_list = list(set(itertools.chain(*plant_list)))
    plant_list.sort()

    while True:
        ask = input(
            'Would you like a specific powerplant? (no/PLANT_NAME/show plants):  ')
        ask = ask.upper()
        if ask in plant_list:
            plant_selected = ask
            chart_label = ask
            country_selected = None
            break
        elif ((ask == 'NO') or (ask == 'N')):
            plant_selected = None
            print('\nall plants selected\n')
            break
        elif ask == 'SHOW PLANTS':
            print('\n', plant_list,
                  '\n\nIf your desired plant is not in this list it means that it was not operational during your date range\n')
        else:
            print('\ninvalid selection')

    if plant_selected == None:
        while True:
            ask = input(
                '\nWould you like a specific country?  (no/COUNTRY_NAME/show countries):  ')
            ask = ask.upper()
            if ask in country_list:
                country_selected = ask
                chart_label = ask
                break
            elif ((ask == 'NO') or (ask == 'N')):
                country_selected = None
                print('\nall countries selected\n')
                chart_label = 'Global'
                break
            elif ask == 'SHOW COUNTRIES':
                print('\n', country_list,
                      '\n\nIf your desired country is not in this list it means they did not have operational plants during your date range\n')
            else:
                print('\ninvalid selection')
    return start_year, end_year, country_selected, plant_selected, chart_label


def ask_user_statistic(plant_selected):
    if plant_selected == None:
        while True:
            ask = input(
                """
        Which statistic would you like to see?

            1 = Actual Power Output
            2 = Available Capacity
            3 = Number of reactors
            4 = Load Factors
            5 = Number of plants
            6 = CO2 emissions
                        
        :   """)
            try:
                statistic = int(ask)
                if statistic in [1, 2, 3, 4, 5, 6]:
                    break
                else:
                    print('invalid input')
            except:
                print('invalid input')
    else:
        while True:
            ask = input(
                """
        Which statistic would you like to see?

            1 = Actual Power Output
            2 = Available Capacity
            3 = Number of reactors
            4 = Load Factors

                        
        :   """)
            try:
                statistic = int(ask)
                if statistic in [1, 2, 3, 4]:
                    break
                else:
                    print('invalid input')
            except:
                print('invalid input')

    print('\nyou have chosen statistic:  ', statistic_dict[statistic], '\n')

    cumulate = False
    if statistic in [1, 6]:
        ask = input('Would you like to see cumulative statistics? (y/n):  ')
        if ask == 'y':
            cumulate = True
    return statistic, cumulate


def gen_matrix(statistic, start_year=1954, end_year=2019, country=None, plant=None, database=Dict):
    # This function takes the user requested years and statistic and country or plant
    # and then queries the database to collect the data then finally outputs a data
    # matrix of the chosen parameters, and then 2 lists of row lables. One containing
    # countries and the other containing plant names.
    matrix = []
    country_labels = []
    plant_labels = []

    for i in range(end_year + 1 - start_year):  # loop over years
        x_array = []
        year = 'Year' + str(start_year + i)
        for j in range(len(database[year])):  # loop over plants
            # Placing the if statements inside the loops increases evaluations
            # however this does not noticeably affect the execution speed of code
            if statistic == 1:
                # use getter functions implemented in the class to return desired data
                x = (database[year][j]).get_powerout()
            elif statistic == 2:
                x = (database[year][j]).get_capacity()
            elif statistic == 3:
                x = (database[year][j]).get_numreactors()
            elif statistic == 4:
                x = (database[year][j]).get_loadfactor()
            elif statistic == 5:
                x = (database[year][j]).get_capacity()
                if x > 0:
                    x = 1  # creates binary if the plant was operational
                else:
                    x = 0
            elif statistic == 6:
                x = (database[year][j]).get_country_emissions()
            elif statistic == 7:
                x = (database[year][j]).get_co2_saved()
            x_array.append(x)
            if i == 0:  # do not get labels for repeat years
                # get labels and add them to list
                country_labels.append((database[year][j]).get_country())
                plant_labels.append((database[year][j]).get_name())
        y = [x_array]
        matrix.append(y)
    # transform the nested list to matrix
    # This matrix contains every plant and every year
    matrix = np.transpose(np.vstack(matrix))

    n = matrix.shape[0]
    to_delete = []
    # if a specific country or plant has been requested we delete
    # the others fromt he matrix and the label lists
    if ((country != None) and (plant == None)):
        for j in range(n):
            # Countries / plants will have same indexing in database and matrix
            if database[year][j].get_country() != country:
                to_delete.append(j)
    elif (plant != None):
        for j in range(n):
            if database[year][j].get_name() != plant:
                to_delete.append(j)

    l = len(to_delete)

    if l > 0:
        # delete rows from matrix
        matrix = np.delete(matrix, to_delete, 0)
        for i in range(l):
            # iterate from the back so that indexing doesnt get fucked
            z = to_delete[l - 1 - i]
            # delete off the label lists
            country_labels.pop(z)
            plant_labels.pop(z)

    return matrix, country_labels, plant_labels


def elim_zero_rows(matrix, country_labels, plant_labels):
    # eliminates the rows that contain only-zeros from the matrix
    # a zero row will be there if the plant was not operational
    # during the date / year range
    to_delete = []
    for i in range(matrix.shape[0]):
        if matrix[i].sum() == 0:
            to_delete.append(i)

    l = len(to_delete)
    if l > 0:
        matrix = np.delete(matrix, to_delete, 0)
        for i in range(l):
            # work from back of list so indexing doesnt get messed up
            z = to_delete[l - 1 - i]
            country_labels.pop(z)
            plant_labels.pop(z)

    return matrix, country_labels, plant_labels


def get_country_list(year, database=Dict):
    # Used to show user what are the countries which had operational
    # reactors during their selected date range
    country_list = []
    year = 'Year' + str(year + 1)
    for j in range(len(database[year])):
        if database[year][j].get_capacity() > 0:
            country = database[year][j].get_country()
            if country not in country_list:
                country_list.append(country)
    return country_list


def get_plant_list(year, database=Dict):
    # Used to show user what are the plants which had operational
    # reactors during their selected date range
    plant_list = []
    year = 'Year' + str(year + 1)
    for j in range(len(database[year])):
        if database[year][j].get_capacity() > 0:
            plant = database[year][j].get_name()
            if plant not in plant_list:
                plant_list.append(plant)
    return plant_list


def plot_timeseries(
        matrix, year_labels, chart_label,
        stat=1, sec_matrix=None, cumulative=False, country_labels=None,
        statistic_dict=statistic_dict, ref_nums_dict=ref_nums_dict, ref_labels_dict=ref_labels_dict):
    # plots the data that the user has requested
    # color list used for reference lines
    colors = ['b', 'g', 'r', 'c', 'm', 'y',
              'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k']
    y_vector = []
    if stat == 6:
        y_2_vector = []

    # sum / average over all plants in the data matrix in each year
    # and turn that sum / average into a vector of y_values
    for y in range(len(year_labels)):
        if stat == 4:  # the load factor must be averaged
            matrix = np.where(matrix != 0, matrix, np.nan)
            y_vector.append(np.nanmean(matrix[:, y]))
        elif stat == 6:  # if carbon stats, form 2 lines
            set_country_labels = list(set(country_labels))
            set_country_labels.sort()
            co2_sum = 0
            for unique in set_country_labels:
                count = 0
                for i in range(len(country_labels)):
                    if ((unique == country_labels[i]) and (count == 0)):
                        count += 1
                        co2_sum += matrix[i, y]
            y_vector.append(co2_sum)
            # y2 is what carbon emissions would be without nuclear so we add 2 lines together
            y_2_vector.append((sec_matrix[:, y].sum()) + y_vector[-1])
        else:  # all other statistics are summed
            y_vector.append(matrix[:, y].sum())

    if cumulative == True:
        # we cumulate the y_vectors if the
        # user has asked for cumulative stats
        y_vector = np.cumsum(y_vector)
        if stat == 6:
            y_2_vector = np.cumsum(y_2_vector)

    # Determine which reference statistics to use
    refs_to_use = []
    if stat == 1:  # Power output shown
        counter = 0
        for i in range(8):
            if ((ref_nums_dict[i] < max(y_vector)) and (counter < 3)):
                counter += 1  # only use 3 references max
                refs_to_use.append(i)
    elif stat == 2:
        counter = 0
        for i in range(8, 12):
            if ((ref_nums_dict[i] < max(y_vector)) and (counter < 3)):
                counter += 1  # only use 3 references max
                refs_to_use.append(i)
    elif stat == 6:
        counter = 0
        for i in range(20, 28):
            if ((ref_nums_dict[i] < max(y_2_vector)) and (counter < 3)):
                counter += 1  # only use 3 references max
                refs_to_use.append(i)

    # plot the main data series
    solid_label = None
    if stat == 6:
        dash_label = 'CO2 emissions IF nuclear replaced by coal'
        solid_label = 'CO2 Emissions - Actual'
        plt.plot(year_labels, y_2_vector, 'k', linestyle='--',
                 linewidth=2, label=dash_label)

    plt.plot(year_labels, y_vector, 'k', linewidth=2, label=solid_label)
    # Plot reference lines. We use a loop because we do not know how many reference
    # lines there will be. Only that it is 3 or less.
    for i in range(len(refs_to_use)):
        plt.hlines(ref_nums_dict[refs_to_use[i]], year_labels[0],
                   year_labels[-1], color=colors[i], label=ref_labels_dict[refs_to_use[i]])

    # label and plot
    plt.xlabel('year')
    plt.ylabel(statistic_dict[stat])
    if cumulative:
        plt.title(chart_label + ' Cumulative ' + statistic_dict[stat + 10])
        plt.fill_between(year_labels, 0, y_vector, color='lightgrey')
    else:
        plt.title(chart_label + ' ' + statistic_dict[stat + 10])

    if stat in [1, 2, 6]:
        plt.legend()

    plt.show()


def plot_scatter(year, export_counter):
    df_pop = pd.read_csv(
        'data/cleaned_data/world_population.csv', index_col=None)

    matrix, country_labels, plant_labels = gen_matrix(1, year, year)

    country_list = list(df_pop['country'])

    output_by_country = []
    for unique in country_list:
        country_output = []
        for i in range(len(country_labels)):
            if country_labels[i] == unique:
                country_output.append(matrix[i])
        country_output = np.sum(country_output)
        output_by_country.append(country_output)

    df = pd.DataFrame()
    df['country'] = country_list
    df['output'] = output_by_country
    pop = list(df_pop[str(year)])
    pop = [x / 1000 for x in pop]  # divide by 1000 to get millions
    df['population'] = pop
    df = df.sort_values(by=['output', 'population'], ascending=False)
    df = df.reset_index(drop=True)

    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k',
              'gray', 'purple', 'olive', 'dodgerblue',
              'orange', 'gold', 'lime', 'pink',
              'brown', 'g', 'r', 'c', 'b', 'r', 'g', 'c', 'm', 'y', 'k', ]

    # Find the value of 10th highest output

    for i in range(df.shape[0]):
        if (i < 15):
            plt.scatter(df.loc[i, 'population'], df.loc[i, 'output'],
                        color=colors[i], label=str(i + 1) + '. ' + df.loc[i, 'country'])
        else:
            plt.scatter(df.loc[i, 'population'], df.loc[i, 'output'],
                        color='lightgray')

    plt.xlabel('Population (millions)')
    plt.ylabel('Annual Nuclear Output (TWh)')
    plt.title(str(year) + ' Nuclear Power Output vs Country Population')
    plt.legend(prop={'size': 7})
    plt.show()

    ask = input(
        '\nExport data as CSV?  (y/n):  ')

    if ask == 'y':
        export_counter += 1  # used to ensure each file has unique name
        df.to_csv('data/exported_data/' + str(year) + ' output_scatter' + '%s.csv' %
                  export_counter, index=False)
        print('export successful.     path: data/exported_data      name: ' + str(year) + ' output_scatter' + '%s.csv' %
              export_counter)

    return export_counter


def process_request(start_year, end_year, country_selected, plant_selected, chart_label, statistic, cumulate, export_counter):
    # This function contains all of the functionality to pull the info from the database and then plot it and then
    # export the data to a CSV file if the user requests to do so.
    if statistic in [1, 2, 3, 4, 5]:
        matrix, country_labels, plant_labels = gen_matrix(
            statistic, start_year, end_year, country_selected, plant_selected)

        matrix, country_labels, plant_labels = elim_zero_rows(
            matrix, country_labels, plant_labels)

        year_labels = np.linspace(start_year, end_year,
                                  end_year - start_year + 1, dtype=int)

        plot_timeseries(matrix, year_labels, chart_label,
                        statistic, cumulative=cumulate)

    else:  # carbon statistic requested
        if ((start_year < 1960) or (end_year > 2017)):
            print(
                'carbon emissions statistics only available in date range [1960, 2017]')
            if start_year < 1960:
                start_year = 1960
            if end_year > 2017:
                end_year = 2017

        # Carbon statistic requires two different datasets because we plot two different lines.
        emissions_matrix, country_labels, plant_labels = gen_matrix(
            statistic, start_year, end_year, country_selected, plant_selected)

        co2_saved_matrix, country_labels, plant_labels = gen_matrix(
            statistic + 1, start_year, end_year, country_selected, plant_selected)

        year_labels = np.linspace(start_year, end_year,
                                  end_year - start_year + 1, dtype=int)

        # The tag "Global" does not make sense in this case since the carbon emissions are
        # not global emissions, but rather just emissions from the countries which have
        # Nuclear power reactors.
        if chart_label == 'Global':
            chart_label = 'All Nuclear Power Countries'

        plot_timeseries(emissions_matrix, year_labels, chart_label,
                        statistic, sec_matrix=co2_saved_matrix, cumulative=cumulate, country_labels=country_labels)

    #######################################################################
    # Export if requested
    #######################################################################

    ask = input(
        '\nExport data as CSV?  (y/n):  ')

    if ask == 'y':
        export_counter += 1  # used to ensure each file has unique name
        if statistic in [1, 2, 3, 4, 5]:
            # create dataframe from the numpy matrix of data
            export = pd.DataFrame(data=matrix, columns=year_labels)
            # add the row labels for plant as the first column
            export.insert(column='plant', loc=0, value=plant_labels)
            # add the row labels for country as the first column
            export.insert(column='country', loc=0, value=country_labels)
            export = export.round(3)  # round all values to 3 decimal places
            # write the CSV file using name of statistic plus the counter value
            export.to_csv('data/exported_data/' + statistic_dict[statistic] + '%s.csv' %
                          export_counter, index=False)
            print('export successful.     path: data/exported_data      name: ' + statistic_dict[statistic] + '%s.csv' %
                  export_counter)

        # carbon statistics require that two different sheets be exported.
        # one sheet contains country's annual carbon emissions, other conatins
        # the CO2 that would be emitted if all Nuclear was replaced by coal
        elif statistic == 6:
            export = pd.DataFrame(data=emissions_matrix, columns=year_labels)
            export.insert(column='country', loc=0, value=country_labels)
            export = export.round(3)
            set_country_labels = list(set(country_labels))
            set_country_labels.sort()

            # there are duplicate rows for each reactor if the country has multiple reactors
            # so we delete those duplicate rows by extracting only the first row for each country
            to_keep = []
            for unique in set_country_labels:  # This is a list of all countries
                count = 0
                # iterate over the rows with duplicates
                for i in range(export.shape[0]):
                    # if we find a match and it is the first match we find we put it in the
                    # keep list and increment the counter.
                    if ((unique == export.loc[i, 'country']) and (count == 0)):
                        count += 1
                        to_keep.append(i)
            export = export.iloc[to_keep, :]  # only keep non-duplicate rows
            export.to_csv('data/exported_data/country_emissions%s.csv' %
                          export_counter, index=False)
            print('export successful.     path: data/exported_data      name: ' + 'country_emissions%s.csv' %
                  export_counter)
            export_counter += 1

            # This sheet does not have the same issues with duplicates so is much simpler to export
            export = pd.DataFrame(data=co2_saved_matrix, columns=year_labels)
            export.insert(column='plant', loc=0, value=plant_labels)
            export.insert(column='country', loc=0, value=country_labels)
            export = export.round(3)
            export.to_csv('data/exported_data/co2_emissions_if_coal%s.csv' %
                          export_counter, index=False)
            print('export successful.     path: data/exported_data      name: ' + 'co2_emissions_if_coal%s.csv' %
                  export_counter)
    return export_counter


def ask_user_year():
    while True:
        flag = False
        ask = input('\nEnter year in range [1970,2018] :  ')
        try:
            year = int(ask)
            if ((year >= 1970) and (year <= 2018)):
                break
            else:
                flag = True
        except:
            print('invalid input')
        if flag:
            print('year not in range')
    return year
