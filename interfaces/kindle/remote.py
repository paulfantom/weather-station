#!/usr/bin/env python

import paramiko
import os

class RemoteDisplay:
  
  def __init__(self,screen):
    self.screen    = screen
    self.ssh       = paramiko.SSHClient()

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
      print ( "Cannot connect do remote device" )

  def send(self,where='/tmp/screen.png'):
    try:
      sftp = self.ssh.open_sftp()
    except Exception:
      print ( "Display not updated" )
      return
    try:
      sftp.put(self.screen,where)
      command = '/usr/sbin/eips -g ' + where
    except OSError:
      print "No file to send"
      
    command = '/usr/sbin/eips -g ' + where
    (stdin, stdout, stderr) = self.ssh.exec_command(command)


  def quit(self):
    command = '/usr/sbin/eips -g /mnt/us/extensions/WeatherStation/bin/TARDIS.jpg'
    (stdin, stdout, stderr) = self.ssh.exec_command(command)
    self.close()

  def close(self):
    self.ssh.close()
    try:
      os.remove(self.screen)
    except OSError:
      print ( "Couldn't remove temporary file" )

  def auto(self):
    self.connect()
    self.send()
    #self.close()
    self.ssh.close()


if __name__ == '__main__':

  kindle = RemoteDisplay('./pic.png')
  kindle.auto()
  try:
    if kindle:
      del kindle
  except NameError:
    pass
