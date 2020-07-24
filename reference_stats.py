#############################################################################
# This contains reference statistics that were found on the internet.
# the purpose of these statistics is to help the user find some sort
# of frame of reference when viewing the nuclear power generation
# statistics. These stats will automatically be plotted on database
# queries.
#############################################################################


# Keys:
# C = Consumption
# P = Production capacity


world_c_2015 = 24255  # TWh from IEA publication in pdfs
china_c_2015 = 5844  # TWh from IEA publication in pdfs
us_c_2017 = 3723  # TWh from spreadsheet
us_p_2017 = 1084370  # MW from spreadsheet
# TWh https://www.cleanenergywire.org/news/total-electricity-consumption-germany-largely-stable-2018
germany_c_2018 = 556.5
california_c_2017 = 257.3  # TWh from spreadsheet
california_p_2017 = 76414  # MW from spreadsheet
illinois_c_2017 = 137.2  # TWh from spreadsheet
illinois_p_2017 = 45147  # MW from spreadsheet
swiss_c_2018 = 57.6  # TWh Swiss Federal Office of Energy
hawaii_c_2017 = 9.3  # TWh from spreadsheet
hawaii_p_2017 = 2718  # MW from spreadsheet

world_co2_2017 = 34740  # Mt C02 from spreadsheet
china_co2_2017 = 9839  # Mt C02
usa_co2_2017 = 5270
japan_co2_2017 = 1205
germany_co2_2017 = 799
france_co2_2017 = 356
netherlands_co2_2017 = 164
swiss_co2_2017 = 40

ref_nums_dict = {
    # consumption statistics
    0: world_c_2015,
    1: china_c_2015,
    2: us_c_2017,
    3: germany_c_2018,
    4: california_c_2017,
    5: illinois_c_2017,
    6: swiss_c_2018,
    7: hawaii_c_2017,

    # production statistics
    8: us_p_2017,
    9: california_p_2017,
    10: illinois_p_2017,
    11: hawaii_p_2017,

    20: world_co2_2017,
    21: china_co2_2017,
    22: usa_co2_2017,
    23: japan_co2_2017,
    24: germany_co2_2017,
    25: france_co2_2017,
    26: netherlands_co2_2017,
    27: swiss_co2_2017
}

ref_labels_dict = {
    0: 'World 2015 consumption',
    1: 'China 2015 consumption',
    2: 'USA 2017 consumption',
    3: 'Germany 2018 consumption',
    4: 'California 2017 consumption',
    5: 'Illinois 2017 consumption',
    6: 'Switzerland 2018 consumption',
    7: 'Hawaii 2017 consumption',


    8: 'USA 2017 all type gen capacity',
    9: 'California 2017 all type gen capacity',
    10: 'Illinois 2017 all type gen capacity',
    11: 'Hawaii 2017 all type gen capacity',

    20: 'Global CO2 Emissions 2017',
    21: 'China CO2 Emissions 2017',
    22: 'USA CO2 Emissions 2017',
    23: 'Japan CO2 Emissions 2017',
    24: 'Germany CO2 Emissions 2017',
    25: 'France CO2 Emissions 2017',
    26: 'Netherlands CO2 Emissions 2017',
    27: 'Swiss CO2 Emissions 2017'
}
