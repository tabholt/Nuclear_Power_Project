#######################################################################
# Initialize the database
#######################################################################

from initialize_database import *

#######################################################################
# Get and process user queries
#######################################################################
export_counter = 0
reset_params = True

ask = input('Time Series or Scatter Data?  (t/s):  ')
if ask == 's':
    while True:
        year = ask_user_year()

        export_counter = plot_scatter(year, export_counter)

        ask = input('\nAnother query?  (y/n):  ')

        if ask != 'y':
            break  # exit the loop therefore terminating program
else:
    while True:

        if reset_params:
            # run function that will ask the user what country / plant / dates they are looking for
            start_year, end_year, country_selected, plant_selected, chart_label = ask_user_params()

        # reset varibale to false for the next cycle
        reset_params = False

        statistic, cumulate = ask_user_statistic(plant_selected)

        export_counter = process_request(start_year, end_year, country_selected,
                                         plant_selected, chart_label, statistic, cumulate, export_counter)

        ask = input('\nAnother query?  (y/n):  ')

        if ask != 'y':
            break  # exit the loop therefore terminating program

        ask = input('\nReset date or country parameters?  (y/n):  ')

        if ask == 'y':
            reset_params = True
