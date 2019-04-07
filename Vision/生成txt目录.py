# 会在当前目录生成一个如图所示的文件，记得修改 w h 为上面修改后的尺寸值
import os


def getimage(file_dir):
    images = {}
    for root, dirs, files in os.walk(file_dir):
        for name in files:
            images[name] = os.path.join(root, name)
    return images


if __name__ == '__main__':
    n = 0
    aa = os.getcwd()
    dirpath = os.path.join(aa, './Actor/izrf')
    imagedic = getimage(dirpath)
    # print(imagedic)

    try:
        for key, value in imagedic.items():
            with open('pos.txt', 'a') as f:
                f.write('./Actor/izrf/' + str(key).rjust(3, '0') + ' 1 0 0 200 200''\n')     #最后两位宽、高要修改为合适
    except KeyboardInterrupt:
        print('暂停一下')