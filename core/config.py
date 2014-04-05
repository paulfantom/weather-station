#!/usr/bin/env python

import ConfigParser
import sys

class Configuration():
  # get values from config file
  def __init__(self,path='./config'):
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    self.config = config
    try:
      config.read(path)
    except Exception:
      print "No config file found"
      print "Terminating"
      sys.exit(1)

  def getKey(self):
  # get API key from config file
    try:
      return self.config.get('weather','APIkey')
    except ConfigParser.NoOptionError:
      return None
    except Exception:
      print "Error parsing config file: [weather] APIkey"
      print "Terminating"
      sys.exit(1)

  def getLocation(self,chooser='weather'):
    if chooser != 'both' and chooser != 'weather' and chooser != 'pollution':
      return None

    if chooser == 'both' or chooser == 'weather':
    # get weather location
      try:
        weatherLocation = self.config.get('weather','location')
      except Exception:
        weatherLocation = 'autoip'
    if chooser == 'both' or chooser == 'pollution':
    # get pollution location
      try:
        pollutionLocation = self.config.get('pollution','location')
      except ConfigParser.NoOptionError:
        pollutionLocation = None
      except Exception:
        print "Error parsing config file: [pollution] location"
        print "Terminating"
    if chooser == 'both':
      return { 'weather'   : weatherLocation,
               'pollution' :pollutionLocation }
    if chooser == 'weather':
      return weatherLocation
    if chooser == 'pollution':
      return pollutionLocation

  def getPollutants(self):
    # get pollutants
    try:
      pollutants = self.config.get('pollution','pollutants')
    except ConfigParser.NoOptionError:
      pollutants = None
    except Exception:
      print "Error parsing config file: [pollution] pollutants"
      print "Terminating"
      sys.exit(1)
    return pollutants

  def getDimensions(self):
  # use remote display device?
    dimensions = { 'x' : 0, 'y' : 0}
    try:
      dimensions['x'] = self.config.get('screen','x')
      dimensions['y'] = self.config.get('screen','y')
    except ConfigParser.NoOptionError:
      dimensions = (600,800)
    except Exception:
      print "Error parsing config file: [screen] x y"
      print "Terminating"
      sys.exit(1)
    return dimensions

  def getFont(self):
    try:
      font = self.config.get('screen','font')
      return str(font)
    except ConfigParser.NoOptionError:
      return "/usr/share/fonts/dejavu/DejaVuSans.ttf"
    except Exception:
      print "Error parsing config file: [screen] font"
      print "Terminating"
      sys.exit(1)

  def getType(self):
    try:
      return self.config.get('screen','type')
    except ConfigParser.NoOptionError:
      return ("kindle")
    except Exception:
      print "Error parsing config file: [screen] type"
      print "Terminating"
      sys.exit(1)

  def getCredentials(self):
    credentials = { 'user'     : 'root',
                    'password' : 'toor',
                    'address'  : '192.168.2.2',
                    'port'     : '22' }
    for key in credentials:
      try:
        credentials[key] = self.config.get('screen',key)
      except ConfigParser.NoOptionError:
        pass
      except Exception:
        print "Error parsing config file: [screen] ".str(key)
        print "Terminating"
        sys.exit(1)
  def getRemote(self):
    try:
      return self.config.get('screen','location')
    except ConfigParser.NoOptionError:
      return "/mnt/base-us/myts/display"
    except Exception:
      print "Error parsing config file: [screen] user"
      print "Terminating"
      sys.exit(1)

