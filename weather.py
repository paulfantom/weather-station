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
      'temp'     :     self.data["current_observation"]["temp_c"],
      'humidity' :     self.data["current_observation"]["relative_humidity"],
      'feeltemp' :     self.data["current_observation"]["feelslike_c"],
      'pressure' :     self.data["current_observation"]["pressure_mb"],
      'presTrend': str(self.data["current_observation"]["pressure_trend"]),
      'sky'      : str(self.data["current_observation"]["weather"]),
      'wind_mph' : int(self.data["current_observation"]["wind_mph"]),
      'wind_kph' : int(self.data["current_observation"]["wind_kph"])
    }

  def forecast(self):
    return {
      "today": {
        'temp_high' :     self.data["forecast"]["simpleforecast"]["forecastday"][0]["high"]["celsius"],
        'temp_low'  :     self.data["forecast"]["simpleforecast"]["forecastday"][0]["low"]["celsius"],
        'humidity'  :     self.data["forecast"]["simpleforecast"]["forecastday"][0]["avehumidity"],
        'sky'       : str(self.data["forecast"]["simpleforecast"]["forecastday"][0]["conditions"]),
        'wind_mph'  : int(self.data["forecast"]["simpleforecast"]["forecastday"][0]["avewind"]["mph"]),
        'wind_kph'  : int(self.data["forecast"]["simpleforecast"]["forecastday"][0]["avewind"]["kph"])
        },
      "tomorrow": {
       'temp_high'  :     self.data["forecast"]["simpleforecast"]["forecastday"][1]["high"]["celsius"],
       'temp_low'   :     self.data["forecast"]["simpleforecast"]["forecastday"][1]["low"]["celsius"],
       'humidity'   :     self.data["forecast"]["simpleforecast"]["forecastday"][1]["avehumidity"],
       'sky'        : str(self.data["forecast"]["simpleforecast"]["forecastday"][1]["conditions"]),
       'wind_mph'   : int(self.data["forecast"]["simpleforecast"]["forecastday"][1]["avewind"]["mph"]),
       'wind_kph'   : int(self.data["forecast"]["simpleforecast"]["forecastday"][1]["avewind"]["kph"])
       },
      "dayafter": {
       'temp_high'  :     self.data["forecast"]["simpleforecast"]["forecastday"][2]["high"]["celsius"],
       'temp_low'   :     self.data["forecast"]["simpleforecast"]["forecastday"][2]["low"]["celsius"],
       'humidity'   :     self.data["forecast"]["simpleforecast"]["forecastday"][2]["avehumidity"],
       'sky'        : str(self.data["forecast"]["simpleforecast"]["forecastday"][2]["conditions"]),
       'wind_mph'   : int(self.data["forecast"]["simpleforecast"]["forecastday"][2]["avewind"]["mph"]),
       'wind_kph'   : int(self.data["forecast"]["simpleforecast"]["forecastday"][2]["avewind"]["kph"])
       }

    }
  

if __name__ == '__main__':
  from pprint import pprint
  w = Weather("PL/Krakow")
  print w.conditions()['sky']
  pprint(w.conditions())
  pprint(w.forecast())
