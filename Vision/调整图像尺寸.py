#coding = utf-8
import scipy
import scipy.misc
from PIL import Image
from pylab import *

imgpath = './pics/pic01.jpg'
im = array(Image.open(imgpath))
print("im.shape:", im.shape)
imshow(im)
axis('off')
title("im")
show()

#scipy.misc.imresize(arr, size, interp='bilinear', mode=None)
# 参数：
# arr: 需要被调整尺寸的图像数组
# size: 整数、浮点或元组
#      整数：当前尺寸的百分比
#      浮点：当前尺寸的分数
#      元组：输出图像的尺寸
# interp: 用于调整大小的插值(应该是调整尺寸的算法吧)
# mode: PIL图像模式(' P '， ' L '等)在调整大小前转换arr。（好像二维数组取值为P,L;三维数组取值为RGB等）
# 返回：
# 调整尺寸后的图像数组

im1 = scipy.misc.imresize(im, 2.0)
print("im1.shape:", im1.shape)
imshow(im)
axis('off')
title("im1")
show()

im2 = scipy.misc.imresize(im, 50, mode='RGB')
print("im2.shape:", im2.shape)
imshow(im)
axis('off')
title("im2")
show()

im3 = scipy.misc.imresize(im, (40, 60,3))
print("im3.shape:", im3.shape)
imshow(im)
axis('off')
title("im3")
show()
