#!/usr/bin/env python

from re       import sub
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
  
    tempForecast = Blocks(smallFont.renderText(  self.weather.forecast()['today']['temp_low']
                                                 + '/'
                                                 + self.weather.forecast()['today']['temp_high']))
    tempCurrent  = Blocks(  bigFont.renderText(  "T: " 
                                                 + self.weather.conditions()['temp'] 
                                                 + " (" 
                                                 + self.weather.conditions()['feeltemp'] 
                                                 + ") "))
  
    tempForecast **= Blocks(smallFont.renderText(  self.weather.forecast()['tomorrow']['temp_low'] 
                                                 + '/' 
                                                 + self.weather.forecast()['tomorrow']['temp_high'])) 
    tempForecast **= Blocks(smallFont.renderText(  self.weather.forecast()['dayafter']['temp_low'] 
                                                 + '/' 
                                                 + self.weather.forecast()['dayafter']['temp_high'])) 
  
    windCurrent  = Blocks(bigFont.renderText(self.weather.conditions()['wind'] + " m/s "))
    windForecast = Blocks(smallFont.renderText(self.weather.forecast()['today']['wind']))
  
    windForecast **= Blocks(smallFont.renderText(self.weather.forecast()['tomorrow']['wind']))
    windForecast **= Blocks(smallFont.renderText(self.weather.forecast()['dayafter']['wind']))
    tempCurrent  &= tempForecast
    tempCurrent.center(self.x)
    windCurrent  &= windForecast
    tempCurrent **= windCurrent.center(self.x)
    
    if self.weather.conditions()['presTrend'] == '0':
      pressureString = self.weather.conditions()['pressure'] + "hpa"
    else:  
      pressureString =  self.weather.conditions()['presTrend'] + " " + self.weather.conditions()['pressure'] + "hpa"
  
    tempCurrent **= Blocks(bigFont.renderText( pressureString )).center(self.x)
  
    if self.weather.conditions()['sky']:
      tempCurrent **= Blocks(bigFont.renderText(sub(r'[^A-Z](.+)\s','. ',self.weather.conditions()['sky']))).center(self.x)
    
    self.tmp = tmp
    tempCurrent.imagine(self.tmp)

  def connect(self,user='root',password='toor',address='192.168.2.2',port=22):
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    self.ssh.connect(address,username=user,password=password,port=port)
    #self.ssh.connect(address,username=user,password=password,port=port,key_filename='/home/paulfantom/.ssh/id_rsa.pub')
    #self.ssh.connect(self.address,username=self.user,password=self.password,port=self.port)

  def send(self,where='/mnt/base-us/myts/display'):
    sftp = self.ssh.open_sftp()
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
