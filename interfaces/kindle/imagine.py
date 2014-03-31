#!/usr/bin/env python
from PIL import Image,ImageDraw,ImageFont,ImageOps

class Block():
  def __init__(self,size=(0,0),background=255,path=None):
    if background > 255:
      self.background = 255
    else:
      self.background = background

    if path:
      self.block = Image.open(path)
    else:
      self.block = Image.new("L",size,background)
#    self.area  = ImageDraw.Draw(self.block)

  def __maxFont(self,text,path,fontSize,lines=1):
    if not fontSize:
      fontSize = 4

    font = ImageFont.truetype(path,fontSize)
    while font.getsize(text)[1] < (self.block.size[1] / lines):
      font = ImageFont.truetype(path,fontSize)
      fontSize += 2

    font = ImageFont.truetype(path,fontSize-6)

    while font.getsize(text)[0] > self.block.size[0]:
      fontSize -= 2
      font = ImageFont.truetype(path,fontSize)

    return { font.getsize(text) : font }

  def __margin(self,first,second,axis='x',justify="center"):
    if axis == 'x':
      axis = 0
    else:
      axis = 1

    if first[axis] < second[axis]:
      a = max(first[axis],second[axis])
      b = min(first[axis],second[axis])
      if justify == "right" or justify == "down":
        return a - b
      if justify == "left" or justify == "up":
        return 0
      else:
        return (a - b) / 2
    else:
      return 0

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

    value      = value.splitlines()
    linesCount = len(value)

    if fontSize == "max":
      fontSize = None

    fonts = {}
    for i in value:
      font = self.__maxFont(i,fontPath,fontSize,linesCount)
      fonts = dict(fonts.items() + font.items())

    minimal = min(fonts.keys(), key = lambda t:t[1])
    font = fonts.get(minimal)

    area  = ImageDraw.Draw(self.block)
    textSize = []
    h = 0
    for line in value:
      textSize.append(area.textsize(line,font))
      h = max(h,textSize[-1][1])
    for i in range(linesCount):
      textSize[i] = (textSize[i][0],h)

    fullH = h * (linesCount + 1 )

    y = self.__margin((textSize[0][0],fullH),self.block.size,'y',vertical)

    for idx,line in enumerate(value):
      x = self.__margin(textSize[idx],self.block.size,'x',horizontal)
      area.text((x,y),line,fill=colour,font=font)
      y += h

    return self

  def join(self,another,where="right",justify="center"):
    background = max(self.background,another.background)
    xSelf     = self.block.size[0]
    ySelf     = self.block.size[1]
    xySelf    = (xSelf, ySelf)
    xAnother  = another.block.size[0]
    yAnother  = another.block.size[1]
    xyAnother = (xAnother, yAnother)

    if where == "up" or where == "down":
      xNew = max(xSelf,xAnother)
      yNew = ySelf + yAnother
    else:
      xNew = xSelf + xAnother
      yNew = max(ySelf,yAnother)

    new = Image.new("L",(xNew,yNew),background)
    if   where == "up":
      coordinatesSelf    = (self.__margin(xySelf,xyAnother,'x',justify),yAnother)
      coordinatesAnother = (self.__margin(xyAnother,xySelf,'x',justify),0)
    elif where == "down":
      coordinatesSelf    = (self.__margin(xySelf,xyAnother,'x',justify),0)
      coordinatesAnother = (self.__margin(xyAnother,xySelf,'x',justify),ySelf)
    elif where == "left":
      coordinatesSelf    = (xAnother,self.__margin(xySelf,xyAnother,'y',justify))
      coordinatesAnother = (0,       self.__margin(xyAnother,xySelf,'y',justify))
    else:          # == "right"
      coordinatesSelf    = (0,    self.__margin(xySelf,xyAnother,'y',justify))
      coordinatesAnother = (xSelf,self.__margin(xyAnother,xySelf,'y',justify))

    new.paste(self.block,   coordinatesSelf)
    new.paste(another.block,coordinatesAnother)

    self.block = new
  
  def grayscale(self,background=None):
    self.block = self.block.convert('L')
    if not background:
      background = self.background
    if background < 128:
      img = self.block
      self.block = ImageOps.invert(img)

  def show(self):
    self.block.show()

  def save(self,path):
    path += ".png"
    self.block.save(path,"png")

if __name__ == '__main__':
  img = Block((300,100),128)
  img2 = Block((200,200),255)
  img2.text("Success\nasdfadsf\nadsgfdgdfs\n9")
  img.text("9 C \n9 km/h",horizontal="center")
  img.join(img2,"right")
  img.show()
