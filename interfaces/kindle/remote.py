#!/usr/bin/env python

#from re       import sub
from imagine import Block
import paramiko
import os

class RemoteDisplay:
  
  def __init__(self,weather,x=600,y=800):
    self.x = x
    self.y = y
    self.weather   = weather
    self.tmp       ='/tmp/weather'
    self.ssh       = paramiko.SSHClient()

  def draw():
    return

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

  def send(self,where='/mnt/us/extensions/bin/'):
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
    self.asciiDisplay(None)
    self.connect()
    self.send()
    self.clear()


if __name__ == '__main__':

  from pprint import pprint

  location = 'PL/Krakow'
  API_KEY="fecfc874ac6ad136"
  weather   = Weather(location,'a',API_KEY)
  pprint(weather)

  #kindle = RemoteDisplay(weather)
  #kindle = draw(weather)
  #kindle.auto()
