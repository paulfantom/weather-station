#!/usr/bin/env python

from pprint import pprint
import sys

class Blocks():
  def __init__(self,string):
    width  = 0
    height = 1
    stop=True
    for i in string:
      if i == '\n':
        height += 1
        stop=False
      if stop:
        width += 1 
    self.block = [[' ' for i in range(width)] for j in range(height)]
   
    width  = 0
    height = 0
    for i in string:
      if i == '\n':
#        self.block[height][width] = ' '
        height += 1
        width = 0
      else:
        self.block[height][width] = i
        width += 1

    # remove if last two lines are the same (prevent double blank line)
    if self.block[len(self.block)-1] == self.block[len(self.block)-2]:
      del(self.block[len(self.block)-1])
  
  def __iand__(self,other):
    # self &= other
    # Horizontal join
    
    #           width      x      height
    leftDim  = ( len(self.block[1]),  len(self.block) )
    rightDim = ( len(other.block[1]), len(other.block) )
    if leftDim[1] > rightDim[1]:
      height = leftDim[0]
    else:
      height = rightDim[0]
    width = leftDim[1] + rightDim[0]

    print rightDim[0]
    # make same height and center smaller in relation to bigger
    # TODO:
    # aligning
    # universal align function

    self.imagine(other)

    return self
  
  def __ipow__(self,other):
    # self **= other
    # Vertical join
  
    #           height     x     width
    upDim   = ( len(self.block), len(self.block[1]) )
    downDim = ( len(other.block), len(other.block[1]) )
    if upDim[1] > downDim[1]:
      width = upDim[1]
    else:
      width = downDim[1]
    height = upDim[0] + downDim[0]

    # make same width
#    if downDim[1] > upDim[1]:
#      for i in range(upDim[0]):
#        for j in range(downDim[1]-upDim[1]):
#          self.block[i].insert(j,' ')
#    elif downDim[1] < upDim[1]:
#      for i in range(downDim[0]):
#        for j in range(upDim[1]-downDim[1]):
#          other.block[i].insert(j,' ')
    self.align(other,downDim,upDim)

    for i in range(downDim[0]):
      self.block.append(other.block[i])
 
    return self
 
  def __add__(self,other):
    width = len(self.block[1])
    import copy
    new = copy.deepcopy(self)
    for i in range(other):
      new.block.insert(i, [' ' for j in range(width)]) 
    return new

  def align(self,obj,(a,b),(c,d),insertion=' '):
    if b > d:
      for i in range(c):
        for j in range(b-d):
          self.block[i].insert(j,insertion)
    elif b < d:
      for i in range(a):
        for j in range(d-b):
          obj.block[i].insert(j,insertion) 
 
  def imagine(self,debug=None):
    height = len(self.block)
    width  = len(self.block[1])
    for i in range(height):
      for j in range(width):
        sys.stdout.write(self.block[i][j])
        if j == width-1:
          print
    if debug:
      print str(height) + " x " + str(width)


if __name__ == '__main__':
  from weather import Weather
  from pyfiglet import Figlet

  weather   = Weather('PL/Krakow')
  bigFont   = Figlet(font='univers')
  smallFont = Figlet(font='straight')

  today    = Blocks(smallFont.renderText(weather.forecast()['today']['temp_low'] + '/' + weather.forecast()['today']['temp_high']))
  tomorrow = Blocks(smallFont.renderText(weather.forecast()['tomorrow']['temp_low'] + '/' + weather.forecast()['tomorrow']['temp_high']))
  #today    = Blocks("alfa\nbeta")
  #tomorrow = Blocks("gamma\nepsil")
  temp     = Blocks(bigFont.renderText("T: " + weather.conditions()['temp'] + "(" + weather.conditions()['feeltemp'] + ")"))
  today **= tomorrow
  temp &= today
