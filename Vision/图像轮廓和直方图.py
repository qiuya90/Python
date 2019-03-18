#coding = utf-8
from PIL import Image
from pylab import *

imgpath = './pics/pic01.jpg'
#添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\windows\fonts\SimSun.ttc", size=14)
im = array(Image.open(imgpath).convert('L'))

figure()
subplot(121)
gray()
contour(im, origin='image')
axis('off')
title(u'图像轮廓', fontproperties=font)

subplot(122)
hist(im.flatten(), 128)
title(u'图像直方图', fontproperties=font)
plt.xlim([0, 300])
plt.ylim([0, 25000])

show()
