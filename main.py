#!/usr/bin/env python
from daemon.config  import Configuration
from daemon.weather import Weather
#from daemon.weather_test import Weather
import sys


if __name__ == '__main__':
  from pprint import pprint

  config = Configuration(path='./config')
  weather = Weather(config.getLocation(),config.getKey(),False)
  try:
    interfaces = config.getType()
  except Exception:
    print "Wrong delimeter in config file: [screen] type. Should be ','"
    sys.exit(1)

  if interfaces.find("kindle") != -1:
    from interfaces.kindle.remote import RemoteDisplay
    from interfaces.kindle.screen import Screen
    size = config.getDimensions()
    font = config.getFont()
    path = Screen(weather,size,font=font)
#    kindle = RemoteDisplay(path)
#    kindle.auto()
  if interfaces.find("web") != -1:
    pass
