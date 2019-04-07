import cv2
import numpy as np

class Kordinat:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Sensor:
    def __init__(self,kordinat1,kordinat2,frame_weight,frame_lenght):
        self.kordinat1=kordinat1
        self.kordinat2=kordinat2
        self.frame_weight=frame_weight
        self.frame_lenght =frame_lenght
        self.mask=np.zeros((frame_weight,frame_lenght,1),np.uint8)
        self.full_mask_area=abs(self.kordinat2.x-self.kordinat1.x)
        cv2.rectangle(self.mask,(self.kordinat1.x,self.kordinat1.y),(self.kordinat2.x,self.kordinat2.y),(255),thickness=cv2.FILLED)
        self.stuation=False
        self.car_number_detected=0


video=cv2.VideoCapture("cartest.mp4")
ret,frame=video.read()
cropped_image= frame[0:450, 0:450]
fgbg=cv2.createBackgroundSubtractorMOG2()                               #比较新的一种动态去背景算法，将运动的部分变为白色，静态背景为黑色，
                                                                        # 受光线影响，光的变化也会被识别为运动，因此需要一个比较稳定的光源比较好
Sensor1 = Sensor(
    Kordinat(1, cropped_image.shape[1] - 35),
    Kordinat(340, cropped_image.shape[1] - 30),
    cropped_image.shape[0],                                             #shape获取多维数组属性，如果是二维，[0]则是行数，[1]为列数
    cropped_image.shape[1])                                             #如果是三维，[0]则是二维数组个数，[1]为行数，[2]为列数

kernel=np.ones((5,5),np.uint8)
font=cv2.FONT_HERSHEY_TRIPLEX

n = 0

while (1):
    ret,frame=video.read()
    # resize frame
    cropped_image= frame[0:450, 0:450]
    # make morphology for frame
    deleted_background=fgbg.apply(cropped_image)
    opening_image=cv2.morphologyEx(deleted_background,cv2.MORPH_OPEN,kernel)           #膨胀算法
    _,bins =cv2.threshold(opening_image,200,255,type=0)         #图像二值化，仅保留0和255，也叫阈值化算法
    # cv2.imshow("bins", bins)
    blurred = cv2.blur(bins, (15, 15))
    _, bins = cv2.threshold(blurred, 100, 255, type=0)
    opening_image = cv2.erode(bins, None, iterations = 4)
    opening_image = cv2.dilate(opening_image, None, iterations = 4)
    cv2.imshow("opening_image", opening_image)

    # detect moving anything
    cnts,hierarchy = cv2.findContours(opening_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)             #获取轮廓
    result=cropped_image.copy()

    zeros_image=np.zeros((cropped_image.shape[0], cropped_image.shape[1], 1), np.uint8)    #zero为建立一个多维数组，1位：建立二维数组的个数，
                                                                                            # 2位：二维数组行，3位：二维数组列

    # detect moving anything with loop
    for cnt in cnts:
        x,y,w,h=cv2.boundingRect(cnt)
        if (w>75 and h>75  and w<400 and h<400 ):
            cv2.rectangle(result,(x,y),(x+w,y+h),(255,0,0),thickness=2)
            rect = cv2.minAreaRect(cnt)                                                    #获取矩形的相关参数 rect[0]中心；[1][0]宽;[1][1]高;rect[2]角度
            # print(rect[0])
            cv2.circle(result, (int(rect[0][0]),int(rect[0][1])), 5, (0,0,255), thickness=4)
            # area = cv2.contourArea(cnt)                                                     # 计算轮廓所包含的面积
            # print(area)
            cv2.rectangle(zeros_image,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)

    # detect whether there is car via bitwise_and
    mask1=np.zeros((zeros_image.shape[0],zeros_image.shape[1],1),np.uint8)
    mask_result=cv2.bitwise_or(zeros_image,zeros_image,mask=Sensor1.mask)
    # cv2.imshow("mask_result", mask_result)

    white_cell_number=np.sum(mask_result==255)
    # detect to control whether car is passing under the red line sensor
    sensor_rate=white_cell_number/Sensor1.full_mask_area
    if sensor_rate>0.9 and sensor_rate<5:
        pass

    # if car is passing under the red line sensor . red line sensor is yellow color.
    if (sensor_rate>=0.9 and  sensor_rate<5 and Sensor1.stuation==False):
        # draw the red line
        cv2.rectangle(result, (Sensor1.kordinat1.x, Sensor1.kordinat1.y), (Sensor1.kordinat2.x, Sensor1.kordinat2.y),
                      (0,255, 0), thickness=cv2.FILLED)
        Sensor1.stuation = True
        n += 1
        print(str(n), "result : ", sensor_rate)
    elif (sensor_rate<0.9 and Sensor1.stuation==True) :
        # draw the red line
        cv2.rectangle(result, (Sensor1.kordinat1.x, Sensor1.kordinat1.y), (Sensor1.kordinat2.x, Sensor1.kordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.stuation = False
        Sensor1.car_number_detected+=1
    else :
        # draw the red line
        cv2.rectangle(result, (Sensor1.kordinat1.x, Sensor1.kordinat1.y), (Sensor1.kordinat2.x, Sensor1.kordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)

    cv2.putText(result,str(Sensor1.car_number_detected),(Sensor1.kordinat1.x,150),font,2,(255,255,255))


    cv2.imshow("video", result)
    # cv2.imshow("mask_result", mask_result)
    # cv2.imshow("zeros_image", zeros_image)
    # cv2.imshow("opening_image", opening_image)

    k=cv2.waitKey(30) & 0xff
    if k == 'q':
        break

video.release()
cv2.destroyAllWindows()
