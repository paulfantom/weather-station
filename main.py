#!/usr/bin/env python

from weather import Weather
from remote  import RemoteDisplay
import ConfigParser
import sys

if __name__ == '__main__':

  # get values from config file

  config = ConfigParser.RawConfigParser(allow_no_value=True)
  try:
    config.read('config')
  except Exception:
    print "No config file found"
    sys.exit(101)

  # get API key from config file
  try:
    apiKey = config.get('weather','APIkey')
  except ConfigParser.NoOptionError:
    apiKey = None
  except Exception:
    print "Weather went wrong"
    apiKey = None

  # get weather location
  try:
    location = config.get('weather','location')
  except Exception:
    location = 'autoip'

  # get pollution location
  try:
    pollutionLocation = config.get('pollution','location')
  except ConfigParser.NoOptionError:
    pollutionLocation = None
  except Exception:
    print "Pollution went wrong"
    pollutionLocation = None

  # get pollutants
  try:
    pollutants = config.get('pollution','pollutants')
  except ConfigParser.NoOptionError:
    pollutants = None
  except Exception:
    print "Pollutants in [pollution] went wrong"
    pollutants = None
  
  # create weather object
  weather = Weather(location,pollutionLocation,apiKey)

  # use remote display device?
  try:
    use = config.getboolean('remote','use')
  except Exception:
    use = False

  if use:
    remote = {}
    try:
      items = config.items('remote')
      for i in items:
        remote.update({i[0]:i[1]})
    except ConfigParser.NoSectionError:
      pass

    dimensions = {}
    for i in 'xy':
      if i in remote:
        dimensions.update({i:int(remote[i])})

    # create kindle object (remote display device)
    kindle = RemoteDisplay(weather,**dimensions)

    # convert regular string weather into ascii image
    kindle.asciiDisplay(pollutants)

    credentials = {}
    for i in ('user','password','address','port'):
      if i in remote:
        if i == 'port':
          remote[i] = int(remote[i])
        credentials.update({i:remote[i]})

    # connect to remote display
    kindle.connect(**credentials)

    if 'location' in remote:
      remoteFile = {'location':remote['location']}
    else:
      remoteFile = {}

    # send ascii image to remote display device
    kindle.send(**remoteFile)

    # clear kindle object [delete?]
    kindle.clear()
