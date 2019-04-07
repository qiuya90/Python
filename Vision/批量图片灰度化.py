from skimage import io, color, img_as_ubyte
import PIL.Image
import numpy as np
import os
import string
def convert_gray(f):
    rgb=io.imread(f)
    gray=color.rgb2gray(rgb)
    gray = img_as_ubyte(gray)                     #将float64转换为unit8
    #dst=transform.resize(gray,(111,256))         #改变图像像素大小
    return gray
datapath ='./Actor/zrf/'
dirName ='./Actor/zrf/'
listName = []
for fileName in os.listdir(dirName):
    if os.path.splitext(fileName)[1] == '.jpeg':
        fileName = os.path.splitext(fileName)[0]
        listName.append(fileName)
str=datapath+'/*.jpeg'
coll = io.ImageCollection(str,load_func=convert_gray)
i = 0
for filename in listName:
    io.imsave(r'./Actor/izrf/'+np.str(filename)+'.jpg',coll[i]) #循环保存图片
    i += 1