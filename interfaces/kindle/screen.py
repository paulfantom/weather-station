#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imagine import Block
from time    import strftime
from urllib  import urlopen
import os

class Screen():
  def __init__(self,\
               weather,\
               size         = (600,800),\
               forecastDays = 4,\
               path         = './images/screen.png',\
               font         = "/usr/share/fonts/dejavu/DejaVuSans.ttf",\
               iconSize     = (50,50)):

    self.path         = path
    self.iconSize     = iconSize 
    self.font         = font
    self.forecastDays = forecastDays
    self.weather      = weather
    if weather.data == None:
      try:
        image   = Block(path=path)
      except IOError:
        image   = Block(size)
      message   = Block((image.size[0],image.size[1]*3/8 - iconSize[1]))
      message.text("Cannot download new weather data\n" + \
                   "\n" + \
                   "Check internet connection", \
                   fontSize = 20,\
                   fontPath = self.font)
      if image.size[1] >= size[1]:
        coords = (size[0]-message.size[0],size[1]-message.size[1])
        image.block.paste(message.block,coords)
      else:
        image.join(message,"down")
    else:
      right  = self.__icon(weather.conditions('icon_url'))
      self.icoSize = right.size
      image = self.__time((size[0]/2,right.size[1]))
      image.join(self.__temperature((size[0]/2,size[1]/4)),"down")
      right.join(self.__windAndPressure((size[0]/2,size[1]/4),trend=False),"down")
      image.join(right,"right")
      image.join(self.__conditions((size[0],size[1]/8)),"down")
      image.join(self.__forecast((size[0],size[1]/4)),"down")
      image.expand(size)
    image.save(path)
    self.path = path


  def __time(self,dimensions):
    hour = strftime("%H:%M")
    return Block(dimensions).text(hour,\
                                  fontSize = 16,\
                                  vertical = "center",
                                  fontPath = self.font)

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
      if icon.size[0] != self.iconSize[0] or icon.size[1] != self.iconSize[1]:
        icon.resize(self.iconSize)
      os.remove(path)

    icon.save(path)
    return icon

  def __temperature(self,dimensions,feel=True):
    currentTemp = self.weather.conditions('temp_c')
    if feel:
      feelTemp = self.weather.conditions('feelslike_c')
      if int(feelTemp) != int(currentTemp):
        dimensions = (dimensions[0],dimensions[1]-self.iconSize[1])

        feels = Block((dimensions[0],self.iconSize[1]))
        feels.text("It feels like " + feelTemp + unicode("°","utf-8"),\
                   vertical = "down",\
                   fontSize = 20,\
                   fontPath = self.font)

    temperature = Block(dimensions).text(str(currentTemp) + unicode("°","utf-8"), \
                                         horizontal = "left",
                                         fontPath = self.font)
    try:
      temperature.join(feels,"down")
    except UnboundLocalError:
      pass

    return temperature

  def __windAndPressure(self,dimensions,trend=True):
    param = [ 'wind_kph','pressure_mb' ]
    if trend:
      param.append('pressure_trend')

    for idx,val in enumerate(param):
      param[idx] = str(self.weather.conditions(param[idx]))

    param[0] += " km/h"
    param[1] += " hpa"

    if trend:
      y = self.icoSize[1]/2
      if param[2] != '+' or param[2] != '-':
        param[2] = "Pressure is stable"
      elif param[2] == '+':
        param[2] = "Pressure is rising"
      else:
        param[2] = "Pressure is falling"
    else:
      y = 0

    dimensions = (dimensions[0],(dimensions[1]-y)/2)

    fontSize = 60
    justify  = "right"
    for idx,val in enumerate(param):
      if idx > 1:
        dimensions = (dimensions[0],y)
        fontSize = 20
        justify  = "center"
      tmp = Block(dimensions).text(val,\
                                   horizontal = justify,\
                                   vertical   = "down",\
                                   fontSize   = fontSize,\
                                   fontPath   = self.font)
      try:
        out.join(tmp,"down")
      except UnboundLocalError:
        out = tmp

    return out

  def __conditions(self,dimensions):
    return Block(dimensions).text(self.weather.conditions('weather'),\
                                  vertical = 'up',\
                                  fontSize = 32,\
                                  fontPath = self.font)

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
               vertical = "up",\
               fontPath = self.font )
      new.join(ico,"down")
      temperature = Block((dimensions[0],dimensions[1]*2))
      temperature.text(str(self.weather.forecast(day,'high','celsius'))+unicode("°","utf-8") + "\n" \
                       "\n" + \
                       str(self.weather.forecast(day,'low','celsius'))+unicode("°","utf-8"),\
                       fontPath = self.font)
      new.join(temperature,"down")
      days.join(new)

    return days
