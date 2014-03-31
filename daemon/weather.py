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
    except Exception:
      self.data = None

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

  def conditions(self,save=False):
    if self.data == None:
      return None
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
    if save:
      self.__save({'conditions' : formatedObservation})
    else:
      return formatedObservation


  def forecast(self,save=False):
    if self.data == None:
      return None
    forecast = self.data["forecast"]["simpleforecast"]["forecastday"]
    formatedForecast = { 'today'    : 0,
                         'tomorrow' : 1,
                         'dayafter' : 2}
    for key,val in formatedForecast.iteritems():
      formatedForecast[key] ={
                              'temp_high' :     forecast[val]["high"]["celsius"],
                              'temp_low'  :     forecast[val]["low"]["celsius"],
                              'humidity'  :     forecast[val]["avehumidity"],
                              'sky'       : str(forecast[val]["conditions"]),
                              'sky_icon'  : str(forecast[val]["icon_url"]),
                              'wind_mph'  : int(forecast[val]["avewind"]["mph"]),
                              'wind_kph'  : int(forecast[val]["avewind"]["kph"]),
                              'weekday'   :     forecast[val]["date"]["weekday_short"]
                             }
    if save:
      self.__save({'forecast' : formatedForecast})
    else:
      return formatedForecast

  def save(self,conditions=True,forecast=False):
    if self.tmpFile:
      if conditions:
        self.conditions(True)
      if forecast:
        self.forecast(True)
    else:
      print ("Cannot save forecast to file")
    


if __name__ == '__main__':
  from pprint import pprint
  weather = Weather("PL/Krakow","fecfc874ac6ad136")
#  pprint(weather.conditions())
  pprint(weather.forecast())
