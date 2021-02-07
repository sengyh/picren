#!/usr/bin/env python3

import os
import sys
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def main():
  latitude = sys.argv[1]
  longitude = sys.argv[2]
  coords = (latitude, longitude)
  print(coords)
  locator = Nominatim(user_agent="myGeocoder")
  location = locator.reverse(coords, language='en')
  print(location.raw['address']['country'])
  print(location.raw['address'])
  return 0

if __name__ == "__main__":
  main()

