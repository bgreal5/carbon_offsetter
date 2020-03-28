import numpy as np
import geopy as gp
from geopy.geocoders import Nominatim
from geopy import distance


class Flight:

    def __init__(self, places=None, flight_class='economy', user_agent="carbon_offsetter"):
        """ Accepts an array of places, len > 1 """
        assert( len(places) > 1 )

        # Init
        self.places = places
        self.geolocator = Nominatim(user_agent=user_agent)
        self.init_dicts = self.init_dicts()

        # Run calcs
        self.run_calcs(places)

    def run_calcs(self, places):
        """ Runner method to do/redo calculations given ordered list of places """
        self.place = places
        self.coords = self.get_coords(self.places)
        self.total_km = self.calc_distance(self.coords)
        self.carbon_eq = self.calc_carbon(self.total_km)
        print("Carbon Emission EQ:", self.carbon_eq)

    def get_coords(self, places):
        """ Takes a list of strings, returns a list of lat,long tuples """
        coords = []

        for place in places:
            loc = self.geolocator.geocode(place)
            tup = (loc.latitude, loc.longitude)
            print(place, tup)
            coords.append(tup)

        return coords

    def calc_distance(self, coords):
        """ Takes a list of latlong tuples and returns a final km total """
        km = 0
        for i in range(len(coords) - 1):
            km += distance.distance(coords[i], coords[i+1]).km
        return km

    def calc_carbon(self, km):
        """ Takes in flight km, returns carbon eq """
        if km < 1500:
            c = self.short_haul_dict
        elif km > 2500:
            c = self.long_haul_dict
        else:
            c = interp_dict(km)

        cw = self.get_cw(c)
        x = km + c['dc']

        term1 = ( c['a'] * x**2 + c['b'] * x + c['c'] ) / ( c['s'] * c['plf'] )
        term2 = ( 1 - c['cf'] ) * cw * ( c['ef'] * c['m'] + c['p'] )
        term3 = ( c['af'] * x ) + c['A']
        emission = term1 * term2 + term3
        return emission

    def interp_dict(self, km):
        denom = 1000
        coeff = km / denom
        constants = {}

        for key in self.short_haul_dict.keys():
            a = self.short_haul_dict[key]
            b = self.long_haul_dict[key]
            diff = abs(b - a)
            new_var = (coeff * diff) + a
            constants[key] = new_var

        return constants

    def get_cw(self, c):
        if 'economy':
            cw = c['econ_cw']
        elif 'business':
            cw = c['busn_cw']
        elif 'first':
            cw = c['fcls_cw']
        else:
            cw = None

        return cw

    def init_dicts(self):
        self.short_haul_dict = {'s': 153.51,
            'plf': .82,
            'dc': 95,
            'cf': .07,
            'econ_cw': .96,
            'busn_cw': 1.26,
            'fcls_cw': 2.4,
            'ef': 3.15,
            'p': .54,
            'm': 2,
            'af': 0.0038,
            'A': 11.68,
            'a': 0,
            'b': 2.714,
            'c': 1166.52,
        }

        self.long_haul_dict = {'s': 280.21,
            'plf': .82,
            'dc': 95,
            'cf': .26,
            'econ_cw': .80,
            'busn_cw': 1.54,
            'fcls_cw': 2.4,
            'ef': 3.15,
            'p': .54,
            'm': 2,
            'af': 0.0038,
            'A': 11.68,
            'a': .0001,
            'b': 7.104,
            'c': 5044.93,
        }
