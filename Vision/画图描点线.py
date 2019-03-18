#coding = utf-8
from PIL import Image
from pylab import *

imgpath = './pics/pic01.jpg'
#添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\windows\fonts\SimSun.ttc", size=14)
im = array(Image.open(imgpath))
figure()

#画坐标轴
subplot(121)
imshow(im)
x = [100, 100, 400, 400]
y = [200, 500, 200, 500]
plot(x, y, 'r*')
plot(x[:3], y[:3])
title(u'绘图01', fontproperties=font)

#不画坐标轴
subplot(122)
imshow(im)
x = [100, 100, 400, 400]
y = [200, 500, 200, 500]
plot(x, y, 'r*')
plot(x[:3], y[:3])
axis('off')
title(u'绘图02', fontproperties=font)

show()