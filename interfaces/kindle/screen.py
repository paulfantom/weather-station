#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imagine import Block
from time    import strftime
from urllib  import urlopen
import os

class Screen():
  def __init__(self,weather,\
               size=(600,800),\
               forecastDays=4,\
               path='./images/screen.png'):

    self.path         = path
    self.iconSize     = (50,50)
    self.forecastDays = forecastDays
    self.weather      = weather
    if not weather.data:
      try:
        image = Block(path=path)
        self.size = image.size
        message = Block((image.size[0],size[1]-image.size[1]))
        message.text("Cannot download new weather data\n" + \
                     "\n" + \
                     "Check internet connection", \
                     fontSize=16)
        image.join(message,"down")
      except IOError:
        print "Cannot download weather data"
        print "No screen.png file to upload"
    else:
      self.size = size
      right  = self.__icon(weather.conditions('icon_url'))
      self.icoSize = right.size
      image = self.__time((size[0]/2,right.size[1]))
      image.join(self.__temperature((size[0]/2,size[1]/4)),"down")
      right.join(self.__windAndPressure((size[0]/2,size[1]/4)),"down")
      image.join(right,"right")
      image.join(self.__conditions((size[0],size[1]/10)),"down")
      image.join(self.__forecast((size[0],size[1]/4)),"down")
      image.show()
    image.save(path)
    self.path = path


  def __time(self,dimensions):
#    hour = Block((screenSize[0]/2,screenSize[1]/20))
    hour = strftime("%H:%M")
    return Block(dimensions).text(hour,\
                                  fontSize=16,\
                                  vertical="center")

  def __icon(self,url):
    splitted = url.split("/")
    name = splitted[-1]
    try:
      path = "./images/" + name.split(".")[0] + ".png"
      icon = Block(path=path)
    except IOError:
      splitted[-2] = "j"
      url = "/".join(splitted)
      f = open("./images/" + name,'wb')
      f.write(urlopen(url).read())
      f.close()
      path= "./images/" + name
      icon = Block(path=path)
      icon.grayscale(0)
      os.remove(path)

    self.iconSize = icon.block.size
    icon.save(path)
    return icon

  def __temperature(self,dimensions,feel=True):
    currentTemp = self.weather.conditions('temp_c')
    if feel:
      feelTemp = self.weather.conditions('feelslike_c')
      if int(feelTemp) != int(currentTemp):
        dimensions = (dimensions[0],dimensions[1]-self.iconSize[1])

        feels = Block((dimensions[0],self.iconSize[1]))
        feels.text("It feels like " + feelTemp + " C",fontSize=16)

    temperature = Block(dimensions).text(str(currentTemp) + " C", \
                                         horizontal = "left")
    try:
      temperature.join(feels,"down")
    except UnboundLocalError:
      pass

    return temperature

  def __windAndPressure(self,dimensions,trend=True):
    print dimensions
    param = [ 'wind_kph','pressure_mb' ]
    if trend:
      param.append('pressure_trend')

    for idx,val in enumerate(param):
      param[idx] = str(self.weather.conditions(param[idx]))

    param[0] += " km/h"
    param[1] += " hpa"

    if param[2]:
      y = self.icoSize[1]/2
    else:
      y = 0
    
    dimensions = (dimensions[0],(dimensions[1]-y)/2)

    if trend:
      if param[2] != '+' or param[2] != '-':
        param[2] = "Pressure is stable"
      elif param[2] == '+':
        param[2] = "Pressure is rising"
      else:
        param[2] = "Pressure is falling"

    fontSize = 60
    justify  = "right"
    for idx,val in enumerate(param):
      if idx > 1:
        dimensions = (dimensions[0],y)
        fontSize /= 1
        justify  = "center"
      tmp = Block(dimensions).text(val,\
                                   horizontal = justify,\
                                   vertical   = "down",\
                                   fontSize   = fontSize)
      try:
        out.join(tmp,"down")
      except UnboundLocalError:
        out = tmp

    return out

  def __conditions(self,dimensions):
    return Block(dimensions).text(self.weather.conditions('weather'),\
                                  vertical='up',\
                                  fontSize=32)

  def __forecast(self,dimensions):
    while True:
      if not self.weather.forecast(self.forecastDays-1,'conditions'):
        self.forecastDays -= 1
      else:
        break

    if self.forecastDays < 1:
      return Block()

    dimensions = (dimensions[0]/self.forecastDays,(dimensions[1]-self.iconSize[1])/3)

    days = Block()
    for day in range(0,self.forecastDays):
      ico = self.__icon(self.weather.forecast(day,'icon_url'))
      # TODO resize icon to self.iconSize
      new = Block(dimensions)
      new.text(self.weather.forecast(day,'date','weekday_short'), \
               fontSize = 30, \
               vertical = "up" )
      new.join(ico,"down")
      temperature = Block((dimensions[0],dimensions[1]*2))
      temperature.text(str(self.weather.forecast(day,'high','celsius')) + "\n" \
                       "\n" + \
                       str(self.weather.forecast(day,'high','celsius')))
      new.join(temperature,"down")
      days.join(new)

    return days
