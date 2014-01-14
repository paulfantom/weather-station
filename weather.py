#!/usr/bin/env python

import urllib2
import urllib
import json
from BeautifulSoup import BeautifulSoup


class Weather:
  def __init__(self,
               location="autoip",
               pollution=None,
               apiKey=None):

    options="conditions/forecast"
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

    try:
      aqicnResponse = urllib2.urlopen("http://aqicn.org/?city="
                                      + pollution
                                      + "&size=xlarge")
      self.aqicn = BeautifulSoup(aqicnResponse.read())
#     EPA table for conversion between AQI and uq/m3 for PM2.5
#     C_low | C_high | I_low | I_high | Category
#     0     | 12.0   | 0     | 50     | Good
#     12.1  | 35.4   | 51    | 100    | Moderate
#     35.5  | 55.4   | 101   | 150    | Unhealthy for Sensitive
#     55.5  | 150.4  | 151   | 200    | Unhealthy
#     150.5 | 250.4  | 201   | 300    | Very Unhealty
#     250.5 | 350.4  | 301   | 400    | Hazardous
#     350.5 | 500.4  | 401   | 500    | Hazardous
      self.EPAtable = {
                       'pm25': ( (0    ,12.0 ,0  ,50 ,'Good'),
                                 (12.1 ,35.4 ,51 ,100,'Moderate'),
                                 (35.5 ,55.4 ,101,150,'Unhealthy for Some Groups'),
                                 (55.5 ,150.4,151,200,'Unhealthy'),
                                 (150.5,250.4,201,300,'Very Unhealthy'),
                                 (250.5,500.4,301,500,'Hazardous')),

                       'pm10': ( (0  ,54 ,0  ,50 ,'Good'),
                                 (55 ,154,51 ,100,'Moderate'),
                                 (155,254,101,150,'Unhealthy for Some Groups'),
                                 (255,354,151,200,'Unhealthy'),
                                 (355,424,201,300,'Very Unhealthy'),
                                 (425,604,301,500,'Hazardous') ),

                       'no2' : ( (0   ,53  ,0  ,50 ,'Good'),
                                 (54  ,100 ,51 ,100,'Moderate'),
                                 (101 ,360 ,101,150,'Unhealthy for Some Groups'),
                                 (361 ,649 ,151,200,'Unhealthy'),
                                 (650 ,1249,201,300,'Very Unhealthy'),
                                 (1250,2049,301,500,'Hazardous') ),

                       'so2' : ( (0  ,35  ,0  ,50 ,'Good'),
                                 (36 ,75  ,51 ,100,'Moderate'),
                                 (76 ,185 ,101,150,'Unhealthy for Some Groups'),
                                 (186,304 ,151,200,'Unhealthy'),
                                 (305,604 ,201,300,'Very Unhealthy'),
                                 (605,1004,301,500,'Hazardous') ),

                       'co'  : ( (0   ,4.4 ,0  ,50 ,'Good'),
                                 (4.5 ,9.4 ,51 ,100,'Moderate'),
                                 (9.5 ,12.4,101,150,'Unhealthy for Some Groups'),
                                 (12.5,15.4,151,200,'Unhealthy'),
                                 (15.5,30.4,201,300,'Very Unhealthy'),
                                 (30.5,50.4,301,500,'Hazardous') )
                      }

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

  def pollution2(self,pollutant='pm10'):
    # pollutant = pm10, pm25, no2, so2, co
    # unit = ug/m3
    if self.aqicn == None:
      return "--"

    value = self.aqicn.find('td', attrs={'id':"cur_" + pollutant}).div.contents[0]

    level=(0,0,0,0,0)
    for row in self.EPAtable[pollutant]:
      if row[2] < int(value) and int(value) < row[3]:
        level=row
        break

# C = (AQI - I_low) * ( C_high - C_low ) / ( I_high - I_low ) + C_low
    try:
      ug = ( int(value) - level[2] )*( level[1] - level[0] )/( level[3] - level[2]) + level[0]
    except Exception:
      ug = 0

    return { 
      'value'      : int(ug),
      'conditions' : level[4]
    }


if __name__ == '__main__':
  from pprint import pprint
  w = Weather("PL/Krakow")
  pprint(w.conditions())
  pprint(w.forecast())
#  pprint(w.pollution())
  pprint(w.pollution2('pm10'))
