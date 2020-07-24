####################  Class creation ####################

# Superclass - Definition of a powerplant and its performance in one year


class Plantyear(object):

    def __init__(self, name=None, country=None, year=None, numreactors=0, capacity=0, loadfactor=0, country_emissions=None):
        self.name = name
        self.country = country
        self.year = year
        self.numreactors = numreactors
        self.capacity = capacity
        self.loadfactor = loadfactor
        self.powerout = (loadfactor / 100) * capacity * \
            24 * 365 / 1000 / 1000  # tera-watt hours
        self.country_emissions = country_emissions
        # the best estimate for carbon intensity of coal production
        # is that 1 MtCO2 is released for ever TWh produced.
        self.co2_saved = self.powerout  # Metric Mega Tonnes CO2

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country

    def get_year(self):
        return self.year

    def get_numreactors(self):
        return self.numreactors

    def get_capacity(self):
        return self.capacity

    def get_loadfactor(self):
        return self.loadfactor

    def get_powerout(self):
        return self.powerout

    def get_country_emissions(self):
        return self.country_emissions

    def get_co2_saved(self):
        return self.co2_saved

    def set_name(self, newname):
        self.name = newname

    def set_country(self, newcountry):
        self.contry = newcountry

    def set_year(self, newyear):
        self.year = newyear

    def set_numreactors(self):
        return self.numreactors

    def set_capacity(self, newcapacity):
        self.capacity = newcapacity

    def set_loadfactor(self, newloadfactor):
        self.loadfactor = newloadfactor

    def set_powerout(self, newpowerout):
        self.powerout = newpowerout

    def set_country_emissions(self, country_emissions):
        self.country_emissions = country_emissions

    def __str__(self):
        data = "Name: %s \nCountry: %s \nYear: %s \nNumber of reactors: %s \nCapacity: %s MW \nLoad Factor: %s %% \nPower Output: %.3f TWh " % (
            self.name, self.country, self.year, self.numreactors, self.capacity, self.loadfactor, self.powerout)
        return data
