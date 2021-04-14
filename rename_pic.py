import sys
import os
import subprocess
import re
import time
import json
import codecs

import pandas as pd
#import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut

from setup_db import Location
import sqlalchemy

def rename_pic(pic, session):
  # use subprocess or another way to parse exif data
  print(pic)
  dtorg = subprocess.Popen(['exiftool', '-datetimeoriginal', '-n', pic],
   stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  subsec = subprocess.Popen(['exiftool', '-subsectimeoriginal', '-n', pic],
   stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  #print(dtorg + subsec)
  if not dtorg or not subsec:
    print('\n')
    #return
  #date_time = (dtorg.split(': ')[1].replace('\n', '').replace(' ', '_') + 
  #            ':' + subsec.split(': ')[1].replace('\n', ''))
  #print(date_time)

  # if no subsec just do

  geocode_on = True
  address = {}
  if geocode_on:
    addr_str = get_address(pic, session)
    if addr_str != '':
      address = json.loads(addr_str)
      # want to collect landmarks if there are any: tourism, amenities, leisure...
      # idea: shove all keys into set traverse through them, if exist make place name
      possible_places = {'amenity', 'leisure',  'tourism', 'building', 'craft', 'historic', 'man_made', 'memorial',
      'natural', 'shop', 'waterway'}
      place = ''
      for place_type in possible_places:
        if place_type in address:
          place = address[place_type] + ' '
          break
      print(place + address['city'] + ' ' + address['country'] + '\n')
    else:
      print("sorry, you don't belong anywhere :(" + '\n')
  return

def get_address(pic, session):
  location_str = ''
  lon_str = subprocess.Popen(['exiftool', '-gpslongitude', '-n', pic], stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  lat_str = subprocess.Popen(['exiftool', '-gpslatitude', '-n', pic], stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  if lon_str and lat_str:
    # precision, 4: 11m accuracy, 3: 110m accuracy
    lon = round(float(re.sub('[^0-9.-]','', lon_str)),4)
    lat = round(float(re.sub('[^0-9.-]','', lat_str)),4)
    coords = (lat, lon)
    print(coords)
    # query db to see if entry already exists
    db_addr = session.query(Location).filter(Location.longitude==lon, Location.latitude==lat).first()
    if db_addr is None:
      print('calling nominatim and creating new entry...')
      locator = Nominatim(user_agent="picren")
      # in case geocoder times out
      address_str = reverse_geocode(coords, locator, attempt=1, max_attempts=5)
      if address_str != 'Timed Out':
        new_location_entry = Location(longitude=lon, latitude=lat, address=address_str)
        session.add(new_location_entry)
        session.commit()
        location_str = address_str
      time.sleep(1)
    else: 
      location_str = db_addr.address
      print('entry exists')

    # 
    # tokyo has exception 
  #print(location_str + '\n')
  return location_str

def reverse_geocode(coords, locator, attempt, max_attempts):  
  # TODO:
  # sanity checking on the coords themselves, 
  # more exceptions, coords are wrong. too many calls to nominatim
  try:
    location = locator.reverse(coords, language='en')
    #print(location.raw)
    address_str = json.dumps(location.raw['address'])
    return address_str
  except GeocoderTimedOut:
    print('nominatim did a fucky wucky')
    if attempt <= max_attempts:
      time.sleep(1)
      attempt+=1
      return reverse_geocode(coords, locator, attempt, max_attempts)
    raise
  return 'Timed Out'



