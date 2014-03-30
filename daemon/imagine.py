#!/usr/bin/env python
from PIL import Image,ImageDraw,ImageFont

class Block():
  def __init__(self,size):
    self.size = size
    self.block = Image.new("L",size)
    self.area  = ImageDraw.Draw(self.block)

  # private:
  def __position(self,
                 horizontal="center",
                 vertical="center",
                 rectangleSize=(0,0)):
    if   horizontal == "center":
      x = ( int(self.block.size[0]) - rectangleSize[0] ) / 2
    elif horizontal == "right":
      x =   int(self.block.size[0]) - rectangleSize[0]
    else:         # == "left"
      x = 0

    if   vertical == "center":
      y = ( int(self.block.size[1]) - rectangleSize[1] ) / 2
    elif vertical == "down":
      y =   int(self.block.size[1]) - rectangleSize[1]
    else:       # == "up"
      y = 0

    return (int(x),int(y))

  def __maxFont(self,text,path):
    size = 12
    font = ImageFont.truetype(path,size)
    while font.getsize(text)[0] < self.block.size[0] - 1:
      size += 2
      font = ImageFont.truetype(path,size)
    while font.getsize(text)[1] > self.block.size[1]:
      size -= 2
      font = ImageFont.truetype(path,size)
    return font

  # public:
  def text(self,
           value,
           font="/usr/share/fonts/dejavu/DejaVuSans.ttf",
           horizontal="center",
           vertical="center",
           fontSize="max"):

    if fontSize == "max":
      font = self.__maxFont(value,font)
    else:
      font = ImageFont.truetype(font,fontSize)

    textSize = self.area.textsize(value,font)

    xy = self.__position(horizontal,vertical,textSize)

    self.area.text(xy,value,fill="white",font=font)

  def join(self,another,orientation="right"):
    return self


  def show(self):
    self.block.show()


if __name__ == '__main__':
  rect = Block((400,100))
  rect.text("hellodupa")
  rect.show()

