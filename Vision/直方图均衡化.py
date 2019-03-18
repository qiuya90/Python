#coding = utf-8
from PIL import Image
from pylab import *
from PCV.tools import imtools

imgpath = './pics/pic01.jpg'
#添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\windows\fonts\SimSun.ttc", size=14)
im = array(Image.open(imgpath).convert('L'))
im2, cdf = imtools.histeq(im)

figure()
subplot(221)
axis('off')
gray()
title(u'原始图像', fontproperties=font)
imshow(im)

subplot(222)
axis('off')
title(u'直方图均衡化后的图像', fontproperties=font)
imshow(im2)

subplot(223)
axis('off')
title(u'原始直方图', fontproperties=font)
#hist(im.flatten(), 128, normed=True)
hist(im.flatten(), 128, density=True)

subplot(224)
axis('off')
title(u'均衡化后的直方图', fontproperties=font)
#hist(im2.flatten(), 128, normed=True)
hist(im2.flatten(), 128, density=True)

show()