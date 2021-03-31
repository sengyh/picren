import sys
import os
import subprocess
import re
import time

import pandas as pd
#import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut

def rename_pic(pic):
  # use subprocess or another way to parse exif data
  print(pic)
  dtorg = subprocess.Popen(['exiftool', '-datetimeoriginal', '-n', pic],
   stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  subsec = subprocess.Popen(['exiftool', '-subsectimeoriginal', '-n', pic],
   stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  print(dtorg + subsec)
  if not dtorg or not subsec:
    print('\n')
    #return
  #date_time = (dtorg.split(': ')[1].replace('\n', '').replace(' ', '_') + 
  #            ':' + subsec.split(': ')[1].replace('\n', ''))
  #print(date_time)

  # if no subsec just do

  geocode_on = True
  if geocode_on:
    reverse_geocode(pic)
  

  return

def reverse_geocode(pic):
  location_str = ''
  lon_str = subprocess.Popen(['exiftool', '-gpslongitude', '-n', pic], stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  lat_str = subprocess.Popen(['exiftool', '-gpslatitude', '-n', pic], stdout=subprocess.PIPE).communicate()[0].decode('ascii')
  if lon_str and lat_str:
    # precision, 4: 1.1m accuracy, 3: 110m accuracy
    lon = round(float(re.sub('[^0-9.-]','', lon_str)),4)
    lat = round(float(re.sub('[^0-9.-]','', lat_str)),4)
    coords = (lat, lon)
    print(coords)
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(coords, language='en')
    print(location)
    location_str = location

    # want to collect landmarks: tourism, places...
    # only collect city and country (if city non existent pick province)
    # tokyo has exception
    print(location.raw['address'].get('tourism'))
    print(location.raw)
    time.sleep(2)

  return location_str
