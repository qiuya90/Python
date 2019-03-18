#coding = utf-8
from PIL import Image
from pylab import *

imgpath = './pics/pic01.jpg'

im = array(Image.open(imgpath))
#imshow(im)
print("Please Click 3 Points")
imshow(im)
x = ginput(3)
print("You clicked:", x)

show()