import numpy as np
from numpy import *
import cv2
import matplotlib.pyplot as plt
from skimage import measure, draw

path = './pic/solor.jpg'
path1 = './pic/solor1.jpg'
path2 = './pic/solor2.jpg'      #和path图片一样


n = 0
global closed


def findOutline(imgpath):
    global closed
    # load the image and convert it to grayscale
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(gray, 50, 255)
    # cv2.imshow("CANNY", canny)

    # blur and threshold the image
    blurred = cv2.blur(canny, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 28, 255, cv2.THRESH_BINARY)

    # cv2.imshow("BLURRED", thresh)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)

    cv2.imshow("CLOSED" + str(n), closed)

    ##########################################################################角点检测
    '''
    harris Corner检测
    1.OpenCV中的函数cv2.cornerHarris()和cv2.cornerSubPix()
    2.cv2.cornerharris()参数：
        img：输入图像，输入图像必须是float32
        blockSize:这是考虑检测的领域大小
        ksize:使用Sobel衍生物的孔径参数
        k:harris Corner检测器的自由参数，在 0.04 到 0.05 之间
    '''
    dst = cv2.cornerHarris(closed, 3, 3, 0.04)
    ##########################################################################获取Harris角点坐标
    keypoints = np.argwhere(dst > 0.01 * dst.max())
    # print(keypoints)

    dst = cv2.dilate(dst, None)                        #对角点进行膨胀
    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    # 找到质心
    ret, labels, states, centroids = cv2.connectedComponentsWithStats(dst)
    # 定义停止和改进角落的标注
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

    # 现在绘制它们
    res = np.hstack((centroids, corners))
    res = np.int0(res)
    # print(res)
    res = delete(res, [0], axis=0)                 #去掉质心点，否则多一个点
    res = res.transpose()
    res = delete(res, [2], axis=0)
    res = delete(res, [2], axis=0)
    res[[0, 1], :] = res[[1, 0], :]               #交换第一二行
    res = res.transpose()
    print(res)
    image[res[:, 0], res[:, 1]] = [0, 0, 255]  # 红色
    # image[res[:, 3], res[:, 2]] = [0, 0, 255]  # 红色

    # image[dst > 0.01 * dst.max()] = [0, 0, 255]          #将角点用红色显示在图像上
    # cv2.imshow('Harris' + str(n), image)

    #检测所有图形的轮廓
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)

    #将轮廓的坐标值输出
    # print(c)
    # for i in c[:][0]:
    #     print(i[0])

    cv2.drawContours(image, c, -1, (0, 0, 255), 1)
    cv2.namedWindow("CLOSED_LINES" + str(n), 0)
    cv2.imshow("CLOSED_LINES" + str(n), image)

    #验证图像相减的效果，为bgr列表相减，255制
    # print(image[220][100])
    # print(image[230][100])
    # print(image[230][100] - image[220][100])
    print("*" * 30)


findOutline(path)
n += 1
img1 = closed
findOutline(path1)
img2 = closed

#直接相减的方法测试图片是否完全相等
difference = cv2.subtract(img1, img2)
result = not np.any(difference) #如果difference全为零，返回值则为False，result置反
if result is False:
    cv2.imshow("DIFFERENCE", difference)
# print(result)

#用像素点判断的方法对比两幅图片有多少像素点差别
height, width = img1.shape
for line in range(height):
    for pixel in range(width):
        if img1[line][pixel] != img2[line][pixel]:
            n = n + 1
# print(n)
m = height * width
# print(m)
print(str(round(n/m, 3)) + "%")

cv2.waitKey(0)