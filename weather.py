#!/usr/bin/env python

import urllib2
import json

class Weather:
  def __init__(self,location="autoip",options="conditions/forecast"):
    wundergroundResponse = urllib2.urlopen(
      "http://api.wunderground.com/api/fecfc874ac6ad136/" + options + "/q/" + location + ".json").read()
    self.data = json.loads(wundergroundResponse)

  def conditions(self):
    return {
      'temp'     : str(    self.data["current_observation"]["temp_c"]),
      'humidity' : str(    self.data["current_observation"]["relative_humidity"]),
      'feeltemp' : str(    self.data["current_observation"]["feelslike_c"]),
      'wind'     : str(int(self.data["current_observation"]["wind_kph"]*4/9)),
      'sky'      : str(    self.data["current_observation"]["weather"])
    }

  def forecast(self):
    return {
      "today": {
        'temp_high' : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["high"]["celsius"]),
        'temp_low'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["low"]["celsius"]),
        'humidity'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["avehumidity"]),
        'wind'      : str(int(self.data["forecast"]["simpleforecast"]["forecastday"][0]["avewind"]["mph"]*4/9)),
        'sky'       : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["conditions"])
        },
      "tomorrow": {
       'temp_high'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["high"]["celsius"]),
       'temp_low'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["low"]["celsius"]),
       'humidity'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["avehumidity"]),
       'wind'       : str(int(self.data["forecast"]["simpleforecast"]["forecastday"][1]["avewind"]["mph"]*4/9)),
       'sky'        : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["conditions"])
       },
      "dayafter": {
       'temp_high'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["high"]["celsius"]),
       'temp_low'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["low"]["celsius"]),
       'humidity'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["avehumidity"]),
       'wind'       : str(int(self.data["forecast"]["simpleforecast"]["forecastday"][2]["avewind"]["mph"]*4/9)),
       'sky'        : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["conditions"])
       }

    }
  

if __name__ == '__main__':
  from pprint import pprint
  w = Weather("PL/Krakow")
  pprint(w.conditions())
  pprint(w.forecast())
