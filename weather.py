#!/usr/bin/env python

import urllib2
import urllib
import json
from BeautifulSoup import BeautifulSoup

#global API_KEY
API_KEY="fecfc874ac6ad136"

class Weather:
  def __init__(self,location="autoip",pollution="Poland/Ma%C5%82opolska/Krak%C3%B3w/AlejaKrasi%C5%84skiego",apikey=API_KEY):
    options="conditions/forecast"
    wundergroundResponse = urllib2.urlopen(
      "http://api.wunderground.com/api/" + apikey + "/" + options + "/q/" + location + ".json").read()
    self.data = json.loads(wundergroundResponse)
    aqicnResponse = urllib2.urlopen("http://aqicn.org/?city=" + pollution + "&size=xlarge")
    self.aqicn = BeautifulSoup(aqicnResponse.read())

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

  def pollution(self):
    return {
      "pm10"        : self.aqicn.find('td', attrs={'id':'cur_pm10'}).div.contents[0],
      "pm25"        : self.aqicn.find('td', attrs={'id':'cur_pm25'}).div.contents[0],
      "no2"         : self.aqicn.find('td', attrs={'id':'cur_no2'} ).div.contents[0],
      "so2"         : self.aqicn.find('td', attrs={'id':'cur_so2'} ).div.contents[0],
      "co"          : self.aqicn.find('td', attrs={'id':'cur_co'}  ).div.contents[0]
    }

  

if __name__ == '__main__':
  from pprint import pprint
  w = Weather("PL/Krakow")
  pprint(w.conditions())
  pprint(w.forecast())
  pprint(w.pollution())
