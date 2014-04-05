#!/usr/bin/env python

import urllib2
import urllib
import json
import time
#from BeautifulSoup import BeautifulSoup


class Weather:
  def __init__(self,
               location="autoip",
               apiKey=None,
               tmpFile=False):

    options="conditions/forecast"
    if tmpFile:
      if type(tmpFile) == str:
        self.tmpFile = tmpFile
      else:
        self.tmpFile = "/tmp/weatherStation.tmp"
    else:
      self.tmpFile = False
    try:
      wundergroundResponse = urllib2.urlopen( "http://api.wunderground.com/api/"
                                             + apiKey
                                             + "/"
                                             + options
                                             + "/q/"
                                             + location
                                             + ".json").read()
      self.data = json.loads(wundergroundResponse)
      if self.data["response"]["error"]:
        print ( "Wrong API key" )
#        raise AttributeError
        self.data = None
    except Exception:
      self.data = None
      print "No weather data available"

  def __save(self,data):
    try:
      with open(self.tmpFile,"r") as fileContent:
        cur = json.load(fileContent)
    except IOError:
      cur = None
    
    try:
      if 'conditions' in data.keys():
        data['forecast'] = cur['forecast']
      else:
        data['conditions'] = cur['conditions']
    except Exception:
      pass

    data['reading date'] = time.strftime("%Y-%m-%d %X")

    with open(self.tmpFile,"w") as fileContent:
      json.dump(data,fileContent,indent=2,sort_keys=True)

  def conditions(self,parameter=None,save=False):
    if self.data == None:
      return None
    if save:
      observation = self.data["current_observation"]
      formatedObservation = {
                           'temp'     :     observation["temp_c"],
                           'humidity' :     observation["relative_humidity"],
                           'feeltemp' :     observation["feelslike_c"],
                           'pressure' :     observation["pressure_mb"],
                           'presTrend': str(observation["pressure_trend"]),
                           'sky'      : str(observation["weather"]),
                           'sky_icon' : str(observation["icon_url"]),
                           'wind_mph' : int(observation["wind_mph"]),
                           'wind_kph' : int(observation["wind_kph"])
                          }
      self.__save({'conditions' : formatedObservation})
    else:
      try:
        return self.data["current_observation"][parameter]
      except KeyError:
        print "Wrong paremeter: " + str(parameter)
        return "---"


  def forecast(self,day,parameter=None,unit=None,save=False):
    if self.data == None:
      return None
    try:
      forecast = self.data["forecast"]["simpleforecast"]["forecastday"][day]
    except IndexError:
      print ( "No forecast for day: " + str(day) )
      return None

    if save:
      formatedForecast = {
                          'temp_high' :     forecast["high"]["celsius"],
                          'temp_low'  :     forecast["low"]["celsius"],
                          'humidity'  :     forecast["avehumidity"],
                          'sky'       : str(forecast["conditions"]),
                          'sky_icon'  : str(forecast["icon_url"]),
                          'wind_mph'  : int(forecast["avewind"]["mph"]),
                          'wind_kph'  : int(forecast["avewind"]["kph"]),
                          'weekday'   :     forecast["date"]["weekday_short"]
                         }
      string = 'forecast day ' + str(day)
      self.__save({string : formatedForecast})

    try:
      forecast = forecast[parameter]
    except KeyError:
      print "Wrong parameter: " + str(parameter)
      return "---"

    if unit:
      try:
        return forecast[unit]
      except KeyError:
        print ( "Wrong unit: " + str(unit) )
        return "--"
      except TypeError:
        return forecast
    else:
      return forecast


  def save(self,conditions=True,forecast=False):
    if self.tmpFile:
      if conditions:
        self.conditions(True)
      if forecast:
        self.forecast(True)
    else:
      print ("No save file specified")
