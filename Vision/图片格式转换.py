#coding=utf-8
from PCV.tools.imtools import get_imlist
from PIL import Image
import os
import pickle

filelist = get_imlist('./pic/')   #获取要转换的文件夹下图片名包括后缀
                                    # (get_imlist仅能识别jpg结尾的图片文件，要获取文件夹下所有文件需要用os.dir)
imlist = open('./pic/imlist.txt', 'wb')  #准备txt将获取的图片信息写入
pickle.dump(filelist, imlist, 0)   #序列化写入
imlist.close()

for infile in filelist:
    outfile = os.path.splitext(infile)[0] + ".png"  #提取文件名和扩展名
    if infile != outfile:
        try:
            Image.open(infile).save(outfile)
        except IOError:
            print("Cannot convert" + infile)




