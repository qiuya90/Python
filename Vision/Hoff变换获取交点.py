# -*- coding: UTF-8 -*-
import cv2
import numpy as np

class Point(object):
    x =0
    y= 0
    # 定义构造方法
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def GetLinePara(line):
    line.a = line.p1.y - line.p2.y
    line.b = line.p2.x - line.p1.x
    line.c = line.p1.x *line.p2.y - line.p2.x * line.p1.y

def GetCrossPoint(l1,l2):
    GetLinePara(l1)
    GetLinePara(l2)
    d = l1.a * l2.b - l2.a * l1.b
    p=Point()
    p.x = (l1.b * l2.c - l2.b * l1.c)*1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a)*1.0 / d
    return p


# 1.加载图片，转为二值图
img = cv2.imread('./pic/outline.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 由于Canny只能处理灰度图，所以将读取的图像转成灰度图。
# cv2.imshow('gray', gray)
hoff = gray.copy()
# 2.1.霍夫直线变换
hoff = cv2.Canny(hoff, 50, 150, apertureSize=3)
cv2.imshow("Hoff-Canny", hoff)
lines = cv2.HoughLines(hoff, 1, np.pi / 180, 118)

# 3.将检测到的画出来
for line in lines:
    rho = line[0][0]  # 第一个元素是距离rho
    theta = line[0][1]  # 第二个元素是角度theta
    print(rho)
    print(theta)
    print("")
    if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):  # 垂直直线
        pt1 = (int(rho / np.cos(theta)), 0)  # 该直线与第一行的交点
        # 该直线与最后一行的焦点
        pt2 = (int((rho - hoff.shape[0] * np.sin(theta)) / np.cos(theta)), hoff.shape[0])

        p1=Point(int(rho / np.cos(theta)), 0)
        p2=Point(int((rho - hoff.shape[0] * np.sin(theta)) / np.cos(theta)), hoff.shape[0])
        vertichalLine1 = Line(p1, p2)

        cv2.line(hoff, pt1, pt2, (255))  # 绘制一条白线
    else:  # 水平直线
        pt1 = (0, int(rho / np.sin(theta)))  # 该直线与第一列的交点
        # 该直线与最后一列的交点
        pt2 = (hoff.shape[1], int((rho - hoff.shape[1] * np.cos(theta)) / np.sin(theta)))

        p1=Point(int(rho / np.cos(theta)), 0)
        p2=Point(int((rho - hoff.shape[0] * np.sin(theta)) / np.cos(theta)), hoff.shape[0])
        horizontalLine1 = Line(p1, p2)

        cv2.line(hoff, pt1, pt2, (255), 1)  # 绘制一条直线
cv2.imshow("HoffLines", hoff)

Pc = GetCrossPoint(vertichalLine1,horizontalLine1)
print("Cross point:", int(Pc.x), int(Pc.y))


cv2.imshow('Result', img)
cv2.waitKey(0)
