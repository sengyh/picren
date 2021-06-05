import json
import re
import time
import subprocess
import sqlalchemy

#import geopandas as gpd
#import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
from src.create_db import Location


def get_address(pic, session):
    location_str = ''
    lon_str = subprocess.Popen(['exiftool', '-gpslongitude', '-n', pic],
                               stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    lat_str = subprocess.Popen(['exiftool', '-gpslatitude', '-n', pic],
                               stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    if lon_str and lat_str:
        # precision, 4: 11m accuracy, 3: 110m accuracy
        lon = round(float(re.sub('[^0-9.-]', '', lon_str)), 4)
        lat = round(float(re.sub('[^0-9.-]', '', lat_str)), 4)
        coords = (lat, lon)
        # print(coords)
        # query db to see if entry already exists
        db_addr = session.query(Location).filter(
            Location.longitude == lon, Location.latitude == lat).first()
        if db_addr is None:
            print('calling nominatim and creating new entry...')
            locator = Nominatim(user_agent="picren")
            # in case geocoder times out
            address_str = reverse_geocode(
                coords, locator, attempt=1, max_attempts=5)
            if address_str != 'Timed Out':
                new_location_entry = Location(
                    longitude=lon, latitude=lat, address=address_str)
                session.add(new_location_entry)
                session.commit()
                location_str = address_str
            time.sleep(1)
        else:
            location_str = db_addr.address
            print('entry exists')
    #print(location_str + '\n')
    return location_str


def reverse_geocode(coords, locator, attempt, max_attempts):
    # TODO:
    # sanity checking on the coords themselves,
    # more exceptions, coords are wrong. too many calls to nominatim
    try:
        location = locator.reverse(coords, language='en')
        # print(location.raw)
        address_str = json.dumps(location.raw['address'])
        return address_str
    except GeocoderTimedOut:
        print('nominatim did a fucky wucky')
        if attempt <= max_attempts:
            time.sleep(1)
            attempt += 1
            return reverse_geocode(coords, locator, attempt, max_attempts)
        raise
    return 'Timed Out'


def process_address(address):
    # return a list based on granularity
    # want to collect landmarks if there are any: tourism, amenities, leisure...
    # shove all keys into set and traverse through them, if exist make place name
    possible_places = {'amenity', 'leisure',  'tourism', 'building', 'craft',
                       'historic', 'man_made', 'memorial', 'natural', 'shop', 'waterway', 'railway'}
    place = ''
    for place_type in possible_places:
        if place_type in address:
            place = address[place_type]
            break

    possible_villages = {'village', 'hamlet', 'locality', 'croft'}
    village = ''
    for village_type in possible_villages:
        if village_type in address:
            village = address[village_type]
            break

    possible_suburbs = {'suburb', 'city_district', 'district', 'quarter',
                        'borough', 'city_block', 'residential', 'commercial', 'industrial', 'houses', 'subdivision', 'allotments'}
    suburb = ''
    for suburb_type in possible_suburbs:
        if suburb_type in address:
            suburb = address[suburb_type]
            break

    possible_cities = {'city', 'town'}
    city = ''
    for city_type in possible_cities:
        if city_type in address:
            city = address[city_type]
            break

    possible_states = {'state', 'province', 'state_code'}
    state = ''
    for state_type in possible_states:
        if state_type in address:
            state = address[state_type]
            break

    # if not state then region, island, archipelago
    if state == '':
        possible_regions = {'region', 'island', 'archipelago'}
        for region_type in possible_regions:
            if region_type in address:
                state = address[region_type]
                break

    country = ''
    if 'country' in address:
        country = address['country']
    else:
        country = address['continent']

    # print(place + village + suburb + city + state + country) #+ '\n')
    # print(address)
    # print('\n')
    #print(place + address['city'] + ' ' + address['country'] + '\n')
    address_list = [place, village, suburb, city, state, country]
    return address_list
