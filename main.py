#!/usr/bin/env python

from weather import Weather
from remote  import RemoteDisplay
import sys

if __name__ == '__main__':

  if len(sys.argv) >1:
    location = sys.argv[1] 
  else:
    location = 'PL/Krakow'
  API_KEY="fecfc874ac6ad136"

  weather   = Weather(location)

  kindle = RemoteDisplay(weather)
  kindle.auto()
  kindle.connect()
