#!/usr/bin/env python

import sys

class Blocks():
  def __init__(self,string):
    width  = 0
    height = 0
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
    
    #           height      x       width
    leftDim  = ( len(self.block),  len(self.block[1]) )
    rightDim = ( len(other.block), len(other.block[1]) )
    if leftDim[0] > rightDim[0]:
      height = leftDim[1]
    else:
      height = rightDim[1]
    width = leftDim[0] + rightDim[1]

    if leftDim[0] < rightDim[0]:
      for i in range(rightDim[0]-leftDim[0]):
        self.block.insert(i,[' ' for j in range(leftDim[1])])
    elif leftDim[0] > rightDim[0]:
      for i in range(leftDim[0]-rightDim[0]):
        other.block.insert(i,[' ' for j in range(rightDim[1])])

    # make same height and center smaller in relation to bigger
    # TODO: center
        
    for i in range(max(leftDim[0],rightDim[0])):
      for j in range(rightDim[1]):
        self.block[i].append(other.block[i][j])

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
#  FIRST
#    if downDim[1] > upDim[1]:
#      for i in range(upDim[0]):
#        for j in range(downDim[1]-upDim[1]):
#          self.block[i].insert(j,' ')
#    elif downDim[1] < upDim[1]:
#      for i in range(downDim[0]):
#        for j in range(upDim[1]-downDim[1]):
#          other.block[i].insert(j,' ')
#  SECOND:
#    if leftDim[0] < rightDim[0]:
#      for i in range(rightDim[0]-leftDim[0]):
#        self.block.insert(i,[' ' for i in range(leftDim[1])])
#    elif leftDim[0] > rightDim[0]:
#      for i in range(leftDim[0]-rightDim[0]):
#        other.block.insert(i,[' ' for i in range(rightDim[1])])
# TODO: UNIFY
#    self.align(other,downDim,upDim)
    if downDim[1] > upDim[1]:
      for i in range(upDim[0]):
        for j in range(downDim[1]-upDim[1]):
          self.block[i].insert(j,' ')
    elif downDim[1] < upDim[1]:
      for i in range(downDim[0]):
        for j in range(upDim[1]-downDim[1]):
          other.block[i].insert(j,' ')

    for i in range(downDim[0]):
      self.block.append(other.block[i])
 
    return self
 
#  def __add__(self,other):
#    width = len(self.block[1])
#    import copy
#    new = copy.deepcopy(self)
#    for i in range(other):
#      new.block.insert(i, [' ' for j in range(width)]) 
#    return new
#
#  def align(self,obj,(a,b),(c,d),insertion=' '):
#    if b > d:
#      for i in range(c):
#        for j in range(b-d):
#          self.block[i].insert(j,insertion)
#    elif b < d:
#      for i in range(a):
#        for j in range(d-b):
#          obj.block[i].insert(j,insertion) 

  def center(self,width):
    diff = width - len(self.block[1])
    if diff <= 0:
      return self
    ldiff = diff/2
    rdiff = ldiff + diff % 2
    for i in range(len(self.block)):
      for j in range(ldiff):
        self.block[i].insert(j,' ')
      for k in range(rdiff):
        self.block[i].append(' ')
    return self

  def trim(self,width,margin='right'):
#    for i in range(0,len(self.block)):
#      if len(self.block[i]) > width:
#        if margin == 'left':
#          self.block[i] = self.block[i][-1-width:-1]
#        elif margin == 'both':
#          self.trim((len(self.block[i])+width)/2,'right')
#          self.trim(width,'left' )
#        else:
#          self.block[i] = self.block[i][0:width]

# less checking (if's excecution) but uglier code:
    if margin == 'left':
      for i in range(0,len(self.block)):
        if len(self.block[i]) > width:
          self.block[i] = self.block[i][-1-width:-1]
    elif margin == 'both':
      for i in range(0,len(self.block)):
        if len(self.block[i]) > width:
          self.trim((len(self.block[i])+width)/2,'right')
          self.trim(width,'left' )
    else:
      for i in range(0,len(self.block)):
        if len(self.block[i]) > width:
          self.block[i] = self.block[i][0:width]

    return self
        

  def imagine(self,path='/tmp/weather',debug=False):
    if not debug:
      temp = sys.stdout
      sys.stdout = open(path, 'w')

    height = len(self.block)
    width  = len(self.block[1])
    for i in range(height):
      for j in range(width):
        sys.stdout.write(self.block[i][j])
        if j == width-1:
          print
    if debug:
      print str(height) + " x " + str(width)
      self.imagine(path,False)
    if not debug:
      sys.stdout.close()
      sys.stdout = temp


if __name__ == '__main__':
  from weather import Weather
  from pyfiglet import Figlet
  from pprint import pprint
  from re import sub

  API_KEY="fecfc874ac6ad136"

  weather   = Weather('PL/Zamosc')
#  weather   = Weather()
  bigFont   = Figlet(font='univers')
  smallFont = Figlet(font='straight')

  tempCurrent  = Blocks(bigFont.renderText("T: " 
                                              + weather.conditions()['temp'] 
                                              + " (" 
                                              + weather.conditions()['feeltemp'] 
                                              + ") "))

  tempCurrent.center(100)
  tempCurrent.trim(80,'both')
  tempCurrent.imagine('/tmp/weather',True)
