#coding = utf-8
from PIL import Image
from pylab import *
from PCV.tools.imtools import get_imlist
from PCV.tools import imtools

#imgpath = './pics/pic01.jpg'
#添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\windows\fonts\SimSun.ttc", size=14)

filelist = get_imlist('./pics/')  #获取文件夹下所有图片
avg = imtools.compute_average(filelist)   #保证图像的像素大小一致，否则会被跳过

for impath in filelist:
    im1 = array(Image.open(impath))
    subplot(2,2,filelist.index(impath)+1)
    imshow(im1)
    inNum = str(filelist.index(impath)+1)
    title(u'待平均图像'+inNum,fontproperties=font)
    axis('off')
subplot(2,2,4)
imshow(avg)
title(u'平均后的图像', fontproperties=font)
axis('off')

show()