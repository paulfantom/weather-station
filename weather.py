#!/usr/bin/env python

import urllib2
import json

#global API_KEY
API_KEY="fecfc874ac6ad136"

class Weather:
  def __init__(self,location="autoip",options="conditions/forecast",apikey=API_KEY):
    wundergroundResponse = urllib2.urlopen(
      "http://api.wunderground.com/api/" + apikey + "/" + options + "/q/" + location + ".json").read()
    self.data = json.loads(wundergroundResponse)

  def conditions(self):
    return {
      'temp'     : str(    self.data["current_observation"]["temp_c"]),
      'humidity' : str(    self.data["current_observation"]["relative_humidity"]),
      'feeltemp' : str(    self.data["current_observation"]["feelslike_c"]),
      'sky'      : str(    self.data["current_observation"]["weather"]),
      'pressure' : str(    self.data["current_observation"]["pressure_mb"]),
      'presTrend': str(    self.data["current_observation"]["pressure_trend"]),
      'wind'     : str(int(self.data["current_observation"]["wind_kph"]*4/9))
    }

  def forecast(self):
    return {
      "today": {
        'temp_high' : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["high"]["celsius"]),
        'temp_low'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["low"]["celsius"]),
        'humidity'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["avehumidity"]),
        'sky'       : str(    self.data["forecast"]["simpleforecast"]["forecastday"][0]["conditions"]),
        'wind'      : str(int(self.data["forecast"]["simpleforecast"]["forecastday"][0]["avewind"]["mph"]*4/9))
        },
      "tomorrow": {
       'temp_high'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["high"]["celsius"]),
       'temp_low'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["low"]["celsius"]),
       'humidity'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["avehumidity"]),
       'sky'        : str(    self.data["forecast"]["simpleforecast"]["forecastday"][1]["conditions"]),
       'wind'       : str(int(self.data["forecast"]["simpleforecast"]["forecastday"][1]["avewind"]["mph"]*4/9))
       },
      "dayafter": {
       'temp_high'  : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["high"]["celsius"]),
       'temp_low'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["low"]["celsius"]),
       'humidity'   : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["avehumidity"]),
       'sky'        : str(    self.data["forecast"]["simpleforecast"]["forecastday"][2]["conditions"]),
       'wind'       : str(int(self.data["forecast"]["simpleforecast"]["forecastday"][2]["avewind"]["mph"]*4/9))
       }

    }
  

if __name__ == '__main__':
  from pprint import pprint
  w = Weather("PL/Krakow")
  print w.conditions()['sky']
  pprint(w.conditions())
  pprint(w.forecast())
