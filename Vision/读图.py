from PIL import Image
from pylab import *

#添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname = r"c:\windows\fonts\SimSun.ttc", size = 14)
figure()

pil_im = Image.open('C:\\Users\\IvanChur\\PycharmProjects\\01_python\\图像处理\\pic\\pic01.JPG')
#gray()
subplot(121)
title(u'原图', fontproperties = font)
axis('off')
imshow(pil_im)

pil_im = Image.open('C:\\Users\\IvanChur\\PycharmProjects\\01_python\\图像处理\\pic\\pic01.JPG').convert('L')
subplot(122)
title(u'灰度图', fontproperties = font)
axis('off')
imshow(pil_im)

show()