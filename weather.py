#!/usr/bin/env python

import urllib2
import urllib
import json
from BeautifulSoup import BeautifulSoup

#global API_KEY
API_KEY="fecfc874ac6ad136"

class Weather:
  def __init__(self,
               location="autoip",
               pollution="Poland/Ma%C5%82opolska/Krak%C3%B3w/AlejaKrasi%C5%84skiego",
               apikey=API_KEY):

    options="conditions/forecast"
    try:
      wundergroundResponse = urllib2.urlopen( "http://api.wunderground.com/api/"
                                             + apikey
                                             + "/"
                                             + options
                                             + "/q/"
                                             + location
                                             + ".json").read()
      self.data = json.loads(wundergroundResponse)
    except Exception:
      self.data = None

    try:
      aqicnResponse = urllib2.urlopen("http://aqicn.org/?city="
                                      + pollution
                                      + "&size=xlarge")
      self.aqicn = BeautifulSoup(aqicnResponse.read())
    except Exception:
      self.aqicn = None

  def conditions(self):
    if self.data == None:
      return None
    current = self.data["current_observation"]
    return {
      'temp'     :     current["temp_c"],
      'humidity' :     current["relative_humidity"],
      'feeltemp' :     current["feelslike_c"],
      'pressure' :     current["pressure_mb"],
      'presTrend': str(current["pressure_trend"]),
      'sky'      : str(current["weather"]),
      'wind_mph' : int(current["wind_mph"]),
      'wind_kph' : int(current["wind_kph"])
    }

  def forecast(self):
    if self.data == None:
      return None
    forecast = self.data["forecast"]["simpleforecast"]["forecastday"]
    return {
      "today": {
        'temp_high' :     forecast[0]["high"]["celsius"],
        'temp_low'  :     forecast[0]["low"]["celsius"],
        'humidity'  :     forecast[0]["avehumidity"],
        'sky'       : str(forecast[0]["conditions"]),
        'wind_mph'  : int(forecast[0]["avewind"]["mph"]),
        'wind_kph'  : int(forecast[0]["avewind"]["kph"])
        },
      "tomorrow": {
       'temp_high'  :     forecast[1]["high"]["celsius"],
       'temp_low'   :     forecast[1]["low"]["celsius"],
       'humidity'   :     forecast[1]["avehumidity"],
       'sky'        : str(forecast[1]["conditions"]),
       'wind_mph'   : int(forecast[1]["avewind"]["mph"]),
       'wind_kph'   : int(forecast[1]["avewind"]["kph"])
       },
      "dayafter": {
       'temp_high'  :     forecast[2]["high"]["celsius"],
       'temp_low'   :     forecast[2]["low"]["celsius"],
       'humidity'   :     forecast[2]["avehumidity"],
       'sky'        : str(forecast[2]["conditions"]),
       'wind_mph'   : int(forecast[2]["avewind"]["mph"]),
       'wind_kph'   : int(forecast[2]["avewind"]["kph"])
       }

    }

  def pollution(self):
    if self.aqicn == None:
      return {
        "pm10"        : "--",
        "pm25"        : "--",
        "no2"         : "--",
        "so2"         : "--",
        "co"          : "--"
      }
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
