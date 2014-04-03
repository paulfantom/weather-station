#!/usr/bin/env python
from   core.config  import Configuration
from   core.weather import Weather
import core.signals as signals
import sys


if __name__ == '__main__':

  signals.setHandler()

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
    dimensions = config.getDimensions()
    font = config.getFont()
    print font
    path = Screen(weather,dimensions,font=font)
#    kindle = RemoteDisplay(path)
#    kindle.auto()
  if interfaces.find("web") != -1:
    pass
