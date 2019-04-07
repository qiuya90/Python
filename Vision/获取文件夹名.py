# -*- coding: utf-8 -*-
import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件

file_name('./pics/')

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root, file))
    return L

# print(file_name('./pics/'))

# 获取所有.txt文件名称,不要后缀
def GetTxtName(dir):
    listName = []
    for fileName in os.listdir(dir):
        if os.path.splitext(fileName)[1] == '.jpg':
            fileName = os.path.splitext(fileName)[0]
            listName.append(fileName)
            print(fileName)
    return listName

for root, dirs, files in os.walk('./pics/'):
    for file in files:
        if os.path.splitext(file)[1] == '.jpg':
            path = os.path.join(root, file)
            name = os.path.splitext(file)[0]
            print(path)
            print(name)