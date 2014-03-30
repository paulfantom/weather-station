#!/usr/bin/env python
from PIL import Image,ImageDraw,ImageFont

class Block():
  def __init__(self,size,background=0):
    if background > 255:
      self.background = 255
    else:
      self.background = background
    self.block = Image.new("L",size,background)
    self.area  = ImageDraw.Draw(self.block)

  def __maxFont(self,text,path):
    size = 0
    while True:
      size += 2
      font = ImageFont.truetype(path,size)
      if font.getsize(text)[0] > self.block.size[0]:
        font = ImageFont.truetype(path,size-2)
        break

    while font.getsize(text)[1] > self.block.size[1]:
      size -= 2
      font = ImageFont.truetype(path,size)

    return font

  def __position(self,
                 horizontal="center",
                 vertical="center",
                 rectangleSize=(0,0),
                 offset=(0,0)):
    if   horizontal == "center":
      x = ( int(self.block.size[0]) - rectangleSize[0] ) / 2
    elif horizontal == "right":
      x =   int(self.block.size[0]) - rectangleSize[0]
    else:         # == "left"
      x = 0

    if   vertical == "center":
      y = ( int(self.block.size[1]) - rectangleSize[1] ) / 2
    elif vertical == "down":  #FIXME
      y =   self.block.size[1] - rectangleSize[1] - int(rectangleSize[1]/3) # WUT?
    else:       # == "up"
      y = 0

    return (int(x+offset[0]),int(y+offset[1]))

  ### -------------------- ###
  def text(self,
           value,
           fontPath="/usr/share/fonts/dejavu/DejaVuSans.ttf",
           horizontal="center",
           vertical="center",
           fontSize="max"):

    if self.background > 128:
      colour = "black"
    else:
      colour = "white"

    value = value.splitlines()

    if fontSize == "max":
      font = self.__maxFont(max(value,key=len),fontPath)
    else:
      font = ImageFont.truetype(fontPath,fontSize)

#    x,y = 0,0
#    for line in value:
#      textSize = self.area.textsize(line,font)
#      x  = max(x,textSize[0])
#      y  = max(y,textSize[1])
#      print x,y
#    textSize = (x,y)
    textSize = self.area.textsize(max(value,key=len),font)

    multipliers = range(len(value))
    if vertical == "down":
      multipliers.reverse()
      multipliers = [x * -1 for x in multipliers]
    elif vertical == "center":     # == "center"
      if len(multipliers)%2 == 1: # odd number
        for i in range(len(value)):
          multipliers[i] = i - int(len(value)/2)
      else: # even number
        for i in range(len(value)):
          multipliers[i] = 1

    for idx,line in enumerate(value):
      offset = multipliers[idx]*textSize[1]
      xy = self.__position(horizontal,vertical,textSize,(0,offset))
      self.area.text(xy,line,fill=colour,font=font)

  def join(self,another,orientation="right"):
    return self


  def show(self):
    self.block.show()


if __name__ == '__main__':
  img = Block((200,300),128)
  img.text("temp\n---\n89deg",vertical="down")
#  img.text("8deg",vertical="down")
  img.show()

