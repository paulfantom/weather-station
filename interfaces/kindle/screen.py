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
  hour.text(strftime("%H:%m"),fontSize=16)
  return hour

def icon(url):
  splitted = url.split("/")
  name = splitted[-1]
  try:
    icon = Block(path="./icons/" + name.split(".")[0] + ".png")
  except IOError:
    splitted[-2] = "j"
    url = "/".join(splitted)
    f = open("./icons/" + name,'wb')
    f.write(urlopen(url).read())
    f.close()
    icon = Block(path="./icons/" + name)
    icon.grayscale(0)
    icon.save("./icons/" + name.split(".")[0])
    os.remove("./icons/" + name)

  return icon

def create(weather,size=(600,800)):
#  screen  = icon(weather.conditions()['sky_icon'])
#  icoSize = screen.block.size
#  screen.join(time(),"left")
  screen = time()
  
#  ico = icon(weather.conditions()['sky_icon'])
#  icoSize = ico.block.size
  icoSize = (50,50)
#  screen.join(ico,"down")

  temperature = Block((size[0]/2,size[1]/2 - size[1]/20 - icoSize[1]))
  value = str(weather.conditions()['temp']) + "C  "
  temperature.text(value)
  temperature.show()

  screen.join(temperature,"down")

  wind = Block((size[0]/2,size[1]/4 - size[1]/10 - size[1]/20))
  wind.text(" " + str(weather.conditions()['wind_kph']) + " km/h ")

  screen.join(wind,"down")

#  feelTemp = Block((size[0]/2,size[1]/10))
#  feelTemp.text(" Feels like: " + str(weather.conditions()['feeltemp']) + "C ",fontSize=12)

#  temperature.join(feelTemp,"down")

  days = Block()
  for name in ('today','tomorrow','dayafter'):
    newIco = icon(weather.forecast()[name]['sky_icon'])
    new = Block((size[0]/6,icoSize[1]))
    new.text(" " + weather.forecast()[name]['weekday'] + " ")
    new.join(newIco,"down")
    temp = Block((new.block.size[0],size[1]/8))
    temp.text(weather.forecast()[name]['temp_high'] + "\n" + \
              "\n" + \
              weather.forecast()[name]['temp_low'])
    new.join(temp,"down")
    try:
      days.join(new)
    except UnboundLocalError:
      pass

  screen.join(days)

  pressure = Block((size[0]*3/4,size[1]/8))
  pressure.text(weather.conditions()['pressure'] + " hpa      ",horizontal='left')
  trend    = Block((size[0] - pressure.block.size[0],pressure.block.size[1]))
  trend.text(   weather.conditions()['presTrend'])
  pressure.join(trend,'right')

  screen.join(pressure,'down')

  conditions = Block((size[0],size[1]-screen.block.size[1]))
  conditions.text(weather.conditions()['sky'],vertical='up',fontSize=20)

  screen.join(conditions,'down')
  path = '/tmp/screen'
  screen.save(path)
  return path + ".png"



if __name__ == '__main__':

  from weather  import Weather
  from pprint import pprint

  location = 'PL/Krakow'
  API_KEY="fecfc874ac6ad136"
  weather = Weather(location,API_KEY)
  create(weather)

