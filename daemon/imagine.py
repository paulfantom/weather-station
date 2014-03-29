#!/usr/bin/env python
from PIL import Image,ImageDraw,ImageFont

class Block():
  def __init__(self,size):
    self.size = size
    self.block = Image.new("L",size)

  def setFont(fontPath="/usr/share/fonts/dejavu/DejaVuSans.ttf",size=self.size[1])
    self.font = ImageFont.truetype(fontPath,size)
    return self

  def text(self,value,anchor="center"):
    write = ImageDraw.Draw(self.block)
    textSize = write.textsize(value,self.font)
    if anchor == "center":
      x = ( int(self.size[0]) - textSize[0] ) / 2
      y = ( int(self.size[1]) - textSize[1] ) / 2
    elif anchor == "up":
      x = ( int(self.size[0]) - textSize[0] ) / 2
      y =   int(self.size[1])
#TODO add more anchors
    elif type(anchor) == tuple:
      x = anchor[0]
      y = anchor[1]


    xy=(int(x),int(y))
    write.text(xy,value,fill="white",font=self.font)
    return self

  def join(self,another,orientation="right"):
    return self





if __name__ == '__main__':
  

