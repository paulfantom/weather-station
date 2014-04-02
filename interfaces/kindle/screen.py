#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imagine import Block
from time    import strftime
from urllib  import urlopen
import os

#def __init__(self,size=(600,800),background=128):
#  self.background = background
#  self.block      = Block(background=background)
#  self.iconSize   = (50,50)
#  self.x          = size[0]
#  self.y          = size[1]

def time(screenSize=(600,800)):
  hour = Block((screenSize[0]/2,screenSize[1]/20))
  hour.text(strftime("%H:%M"),fontSize=16,vertical="down")
  hour.show()
  return hour

def icon(url):
  splitted = url.split("/")
  name = splitted[-1]
  try:
    path = "./images/" + name.split(".")[0] + ".png"
    icon = Block(path="./images/" + name.split(".")[0] + ".png")
  except IOError:
    splitted[-2] = "j"
    url = "/".join(splitted)
    f = open("./images/" + name,'wb')
    f.write(urlopen(url).read())
    f.close()
    name = "./images/" + name
    icon = Block(path=name)
    icon.grayscale(0)
    os.remove(name)

  return icon

def create(weather,size=(600,800),forecastDays=None):
  
# current weather icon:
  if not weather.data:
    path = './images/screen.png'
    if os.path.isfile(path):
      screen  = Block(path=path)
      message = Block((screen.block.size[0],size[1]-screen.block.size[1]))
      message.text("Cannot download new weather data",fontSize=16)
      screen.join(message,"down")
      screen.save(path)
      return path
    print "Cannot download new weather data"
    return ""

  screen = icon(weather.conditions('icon_url'))
  icoSize = screen.block.size
 
  # wind and pressure:
  wind     = str(weather.conditions('wind_kph'))    + " km/h"
  pressure = str(weather.conditions('pressure_mb')) + " hpa"
  trend    = str(weather.conditions('pressure_trend'))
  if trend != '+' or trend != '-':
    trend = "Pressure is stable"
  elif trend == '+':
    trend = "Pressure is rising"
  else:
    trend = "Pressure is falling"

  for i in (wind,pressure):
    tmp = Block((size[0]/2,size[1]/8-icoSize[1]/2))
    tmp.text(i,horizontal="right",vertical="down",fontSize=60)
    screen.join(tmp,"down","center")

  tmp = Block((size[0]/2,icoSize[1]))
  tmp.text(trend,fontSize=16,vertical="up")
  screen.join(tmp,"down")

  # time and temperature:
  left = time()
  temperature = Block((size[0]/2,screen.block.size[1] - left.block.size[1]))
  temperature.text(str(weather.conditions('temp_c')) + " C ",horizontal = "left")
  left.join(temperature,"down","center")

  screen.join(left,"left")

  # forecast
  days = Block()
  if not forecastDays:
    forecastDays = 4
  while True:
    if not weather.forecast(forecastDays-1,'conditions'):
      forecastDays -=1
    else:
      break

  if forecastDays > 0:
    for day in range(0,forecastDays):
      newIco = icon(weather.forecast(day,'icon_url'))
      new = Block((size[0]/forecastDays,icoSize[1]))
      new.text(weather.forecast(day,'date','weekday_short'),\
               fontSize=30,\
               vertical="up")
      new.join(newIco,"down")
      temp = Block((new.block.size[0],size[1]/8))
      temp.text(str(weather.forecast(day,'high','celsius')) + "\n" + \
              "\n" + \
              str(weather.forecast(day,'low','celsius')))
      new.join(temp,"down")
      days.join(new)
  
    screen.join(days,"down","center")

  # save
  
  path = './images/screen.png'
  screen.expand(size)
  screen.save(path)
  return path

