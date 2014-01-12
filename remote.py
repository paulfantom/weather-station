#!/usr/bin/env python

#from re       import sub
from asciiArt import Blocks
from pyfiglet import Figlet
import paramiko
import os

class RemoteDisplay:
  
  def __init__(self,weather,x=100,y=55):
    self.x = x
    self.y = y
    self.weather = weather
    self.ssh = paramiko.SSHClient()

  def asciiDisplay(self,tmp='/tmp/weather'):
    bigFont   = Figlet(font='univers')
    smallFont = Figlet(font='straight')
  
    temperatureBig    = ( "t " 
                        + str(self.weather.conditions()['temp']) 
                        + "(" + str(self.weather.conditions()['feeltemp']) 
                        + ")" )
    temperatureSmall1 = ( str(self.weather.forecast()['today']['temp_low']) 
                        + '/' 
                        + str(self.weather.forecast()['today']['temp_high']) ) 
    temperatureSmall2 = ( str(self.weather.forecast()['tomorrow']['temp_low']) 
                        + '/' 
                        + str(self.weather.forecast()['tomorrow']['temp_high']))
    temperatureSmall3 = ( str(self.weather.forecast()['dayafter']['temp_low']) 
                        + '/' 
                        + str(self.weather.forecast()['dayafter']['temp_high']))

    if len(temperatureBig) > 8 :
      temperatureBig = "t " + str(self.weather.conditions()['temp'])
    elif len(temperatureBig) == 8 and max(len(temperatureSmall1),
                                           len(temperatureSmall2),
                                           len(temperatureSmall3)) > 5:
      temperatureBig = "t " + str(self.weather.conditions()['temp'])
      
    display    = Blocks(  bigFont.renderText( temperatureBig ))
    tempForecast   = Blocks(smallFont.renderText( temperatureSmall1 ))
    tempForecast **= Blocks(smallFont.renderText( temperatureSmall2 ))
    tempForecast **= Blocks(smallFont.renderText( temperatureSmall3 ))
   
    windCurrent  = Blocks(bigFont.renderText(str(self.weather.conditions()['wind_mph'] * 4/9) + " m/s "))
    windForecast = Blocks(smallFont.renderText(str(self.weather.forecast()['today']['wind_mph'] * 4/9)))
  
    windForecast **= Blocks(smallFont.renderText(str(int(self.weather.forecast()['tomorrow']['wind_mph'])*4/9)))
    windForecast **= Blocks(smallFont.renderText(str(int(self.weather.forecast()['dayafter']['wind_mph'])*4/9)))
    display  &= tempForecast
    display.center(self.x).trim(self.x)
    windCurrent  &= windForecast
    display **= windCurrent.center(self.x).trim(self.x)
    
    if self.weather.conditions()['presTrend'] == '0':
      pressureString = str(self.weather.conditions()['pressure']) + "hpa"
    else:  
      pressureString = ( self.weather.conditions()['presTrend']
                      + " "
                      + str(self.weather.conditions()['pressure'])
                      + "hpa")
  
    display **= Blocks(bigFont.renderText( pressureString )).center(self.x).trim(self.x)
  
    if self.weather.conditions()['sky']:
      conditions = self.weather.conditions()['sky']
      try:
        pos = conditions.rindex(' ')
        small      = conditions[0:pos]  # max 41 chars
        conditions = conditions[pos+1:len(conditions)]
        display **= Blocks(smallFont.renderText(small)).center(self.x)
      except ValueError:
        pass
#      if len(conditions) > 9:
#        conditions = sub(r'[^A-Z](.+)\s','. ',self.weather.conditions()['sky'])
#        if len(conditions) > 9:
#          conditions = conditions[3:12]
      display **= Blocks(bigFont.renderText(conditions)).center(self.x).trim(self.x)
    
    display **= Blocks(smallFont.renderText("Pollution " 
                                            + self.weather.pollution()['pm10'])).center(self.x)
    self.tmp = tmp
    display.imagine(self.tmp)

  def connect(self,user='root',password='toor',address='192.168.2.2',port=22):
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      self.ssh.connect(address,
                       username=user,
                       password=password,
                       port=port,
                       timeout=4)
      #self.ssh.connect(self.address,
      #                 username=self.user,
      #                 password=self.password,
      #                 port=self.port
      #                 timeout=4)
    except Exception:
      print "Cannot connect do remote device"

  def send(self,where='/mnt/base-us/myts/display'):
    try:
      sftp = self.ssh.open_sftp()
    except Exception:
      print "Display not updated"
      return

    sftp.put(self.tmp,where)

  def clear(self):
    self.ssh.close()
    try:
      os.remove(self.tmp)
    except OSError, e:
      print "Couldn't remove temporary file"

  def auto(self):
    self.asciiDisplay()
    self.connect()
    self.send()
    self.clear()
#    self.__del__()


if __name__ == '__main__':

  from weather  import Weather

  location = 'PL/Krakow'
  API_KEY="fecfc874ac6ad136"
  weather   = Weather(location)

  kindle = RemoteDisplay(weather)
  kindle.auto()
