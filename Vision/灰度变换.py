#coding = utf-8
from PIL import Image
from pylab import *

imgpath = './pics/pic01.jpg'
im = array(Image.open(imgpath).convert('L'))
print(int(im.min()), int(im.max()))

im2 = 255 - im  #invert image
print(int(im2.min()), int(im2.max()))

im3 = (100.0/255) * im + 100 # clamp to interval 100...200
print(int(im3.min()), int(im3.max()))

im4 = 255.0 * (im/255.0)**2  #squared
print(int(im4.min()), int(im4.max()))

figure()
gray()
subplot(131)
imshow(im2)
axis('off')
title(r'$f(x)=255-x$')

subplot(132)
imshow(im3)
axis('off')
title(r'$f(x)=\frac{100}{255}x+100$')

subplot(133)
imshow(4)
axis('off')
title(r'$f(x)=255(\frac{x}{255})^2$')

show()