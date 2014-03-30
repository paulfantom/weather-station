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

  def __maxFont(self,text,path,lines=1):
    fontSize = 0
    while True:
      fontSize += 2
      font = ImageFont.truetype(path,fontSize)
      if font.getsize(text)[0] > self.block.size[0] :
        font = ImageFont.truetype(path,fontSize-2)
        break

    while font.getsize(text)[1] > self.block.size[1] / lines:
      fontSize -= 2
      font = ImageFont.truetype(path,fontSize)

    return font

  def __position(self,
                 horizontal="center",
                 vertical="center",
                 rectangleSize=(0,0),
                 offset=(0,0)):
    if   horizontal == "center":
      x = ( self.block.size[0] - rectangleSize[0] ) / 2
    elif horizontal == "right":
      x =   self.block.size[0] - rectangleSize[0]
    else:         # == "left"
      x = 0

    if   vertical == "center":
      y = ( self.block.size[1] - rectangleSize[1] ) / 2
    elif vertical == "down":
      y =   self.block.size[1] - rectangleSize[1]
    else:       # == "up"
      y = 0

    y -= int(rectangleSize[1]/4) #FIXME dafuq is this???
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
      font = self.__maxFont(max(value,key=len),fontPath,len(value))
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
    background = min(self.background,another.background)
    if orientation == "up" or orientation == "down":
      x = max(self.block.size[0], another.block.size[0])
      y = self.block.size[1] + another.block.size[1]
    else:
      x = self.block.size[0] + another.block.size[0]
      y = max(self.block.size[1], another.block.size[1])

    new = Image.new("L",(x,y),background)
    if   orientation == "up":
      new.paste(self.block,(0,another.block.size[1]))
      new.paste(another.block,(0,0))
    elif orientation == "down":
       new.paste(self.block,(0,0))
       new.paste(another.block,(0,self.block.size[1]))
    elif orientation == "left":
      new.paste(self.block,(another.block.size[0],0))
      new.paste(another.block,(0,0))
    else:          # == "right"
      new.paste(self.block,(0,0))
      new.paste(another.block,(self.block.size[0],0))

    self.block = new

  def show(self):
    self.block.show()


if __name__ == '__main__':
  img = Block((300,200),128)
  img2 = Block((300,200),255)
  img2.text("Success")
  img.text("Test\nended\nwith:")
#  img.text("8deg",vertical="down")
  img.join(img2,"down")
  img.show()
#  img.show()
