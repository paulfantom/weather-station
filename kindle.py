#!/usr/bin/env python

from weather  import Weather
from re       import sub
import sys

def asciiDisplay(path):
  from asciiArt import Blocks
  from pyfiglet import Figlet
  bigFont   = Figlet(font='univers')
  smallFont = Figlet(font='straight')

  tempForecast = Blocks(smallFont.renderText(  weather.forecast()['today']['temp_low']
                                               + '/'
                                               + weather.forecast()['today']['temp_high']))
  tempCurrent  = Blocks(  bigFont.renderText(  "T: " 
                                               + weather.conditions()['temp'] 
                                               + " (" 
                                               + weather.conditions()['feeltemp'] 
                                               + ") "))

  tempForecast **= Blocks(smallFont.renderText(  weather.forecast()['tomorrow']['temp_low'] 
                                               + '/' 
                                               + weather.forecast()['tomorrow']['temp_high'])) 
  tempForecast **= Blocks(smallFont.renderText(  weather.forecast()['dayafter']['temp_low'] 
                                               + '/' 
                                               + weather.forecast()['dayafter']['temp_high'])) 

  windCurrent  = Blocks(bigFont.renderText(weather.conditions()['wind'] + " m/s "))
  windForecast = Blocks(smallFont.renderText(weather.forecast()['today']['wind']))

  windForecast **= Blocks(smallFont.renderText(weather.forecast()['tomorrow']['wind']))
  windForecast **= Blocks(smallFont.renderText(weather.forecast()['dayafter']['wind']))
  tempCurrent  &= tempForecast
  tempCurrent.center(SCREEN_X)
  windCurrent  &= windForecast
  tempCurrent **= windCurrent.center(SCREEN_X)
  
  if weather.conditions()['presTrend'] == '0':
    pressureString = weather.conditions()['pressure'] + "hpa"
  else:  
    pressureString =  weather.conditions()['presTrend'] + " " + weather.conditions()['pressure'] + "hpa"

  tempCurrent **= Blocks(bigFont.renderText( pressureString )).center(SCREEN_X)

  if weather.conditions()['sky']:
    tempCurrent **= Blocks(bigFont.renderText(sub(r'[^A-Z](.+)\s','. ',weather.conditions()['sky']))).center(SCREEN_X)

  tempCurrent.imagine(path)

def send(user,passwd,lpath,rpath='/mnt/base-us/myts/display',addr='192.168.2.2'):
  import paramiko
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #ssh.connect(addr,username=user,password=passwd,key_filename='/home/paulfantom/.ssh/id_rsa.pub')
  ssh.connect(addr,username=user,password=passwd,timeout=4)
  sftp = ssh.open_sftp()
  sftp.put(lpath,rpath)
  ssh.close()

def kindle(user,passwd,path):
  global SCREEN_X
  global SCREEN_Y
  SCREEN_X = 100
  SCREEN_Y = 55

  asciiDisplay(path)
  send(user,passwd,path)

if __name__ == '__main__':

  if len(sys.argv) >1:
    location = sys.argv[1] 
  else:
    location = 'PL/Krakow'
  API_KEY="fecfc874ac6ad136"

  weather   = Weather(location)

  kindle('root','toor','/tmp/weather')
