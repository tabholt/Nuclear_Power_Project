#############################################################################
# create_gif.py
# this program runs the scatter plot generator in a loop over all of the
# available years of data in order to generate the frames to create a
# gif of nuclear power ouput vs country population
#
#
# USED BY: not called elsewhere in program
#############################################################################


from initialize_database import *

color_dict = {
    'USA': 'b',
    'FRANCE': 'g',
    'JAPAN': 'k',
    'RUSSIA': 'm',
    'CHINA': 'r',
    'SOUTH KOREA': 'c',
    'CANADA': 'pink',
    'GERMANY': 'gold',
    'UKRAINE': 'y',
    'UNITED KINGDOM': 'dodgerblue',
    'SPAIN': 'purple',
    'SWEDEN': 'olive',
    'TAIWAN, CHINA': 'maroon',
    'INDIA': 'orange',
    'CZECH REPUBLIC': 'thistle',
    'BELGIUM': 'brown',
    'FINLAND': 'deeppink',
    'SWITZERLAND': 'chartreuse',
    'HUNGARY': 'lightcoral',
    'BULGARIA': 'darkslategray',
    'SLOVAKIA': 'chocolate',
    'BRAZIL': 'darkslateblue',
    'ITALY': 'teal',
    'MEXICO': 'thistle',
    'SOUTH AFRICA': 'midnightblue',
    'ROMANIA': 'orchid',
    'ARGENTINA': 'peachpuff',
    'SLOVENIA': 'darkblue',
    'PAKISTAN': 'lightgrey',
    'NETHERLANDS': 'limegreen',
    'IRAN, ISLAMIC REPUBLIC OF': 'lightgrey',
    'ARMENIA': 'hotpink',
    'KAZAKHSTAN': 'wheat',
    'LITHUANIA': 'tomato'
}

my_dpi = 96 * 2

for n in range(49):
    year = 1970 + n
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
    for c in range(len(country_list)):
        if country_list[c] == 'UNITED STATES OF AMERICA':
            country_list[c] = 'USA'
        if country_list[c] == 'KOREA, REPUBLIC OF':
            country_list[c] = 'SOUTH KOREA'

    df = pd.DataFrame()
    df['country'] = country_list
    df['output'] = output_by_country
    pop = list(df_pop[str(year)])
    pop = [(x / 1000) for x in pop]
    df['population'] = pop
    df = df.sort_values(by=['output', 'population'], ascending=False)
    df = df.reset_index(drop=True)

    # Find the value of 10th highest output
    fig = plt.figure(figsize=(480 * 2 / my_dpi, 480 * 2 / my_dpi), dpi=my_dpi)

    for i in range(df.shape[0]):
        if (i < 15):
            plt.scatter(df.loc[i, 'population'], df.loc[i, 'output'],
                        color=color_dict[df.loc[i, 'country']], label=str(i + 1) + '. ' + df.loc[i, 'country'])
        elif ((i >= 15) and (df.loc[i, 'country'] == 'SWITZERLAND')):
            plt.scatter(df.loc[i, 'population'], df.loc[i, 'output'],
                        color=color_dict[df.loc[i, 'country']], label=str(i + 1) + '. ' + df.loc[i, 'country'])
        else:
            plt.scatter(df.loc[i, 'population'], df.loc[i, 'output'],
                        color='lightgray')

    plt.xlabel('Population (millions)')
    plt.xlim(-10, 1460)
    plt.ylim(-10, 875)
    plt.ylabel('Annual Nuclear Output (TWh)')
    plt.title(
        str(year) + ' Nuclear Power Output vs Country Population')
    plt.legend(prop={'size': 7}, loc='upper right')
    num_str = str(n).zfill(2)
    filename = 'data/gif/frame' + num_str + '.png'
    plt.savefig(filename, dpi=my_dpi)
    plt.gca()

# create animated gif using BASH with imagemagick installed
# BASH command:
# $ convert -delay 40 *.png animated_chart.gif
