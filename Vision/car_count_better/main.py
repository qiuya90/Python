import cv2
import numpy as np
import vehicles
import time

cnt_up=0
cnt_down=0


cap=cv2.VideoCapture("surveillance.m4v")

#Get width and height of video

w=cap.get(3)
h=cap.get(4)
frameArea=h*w
areaTH=frameArea/400

#Lines
line_up=int(2*(h/5))
line_down=int(3*(h/5))

up_limit=int(1*(h/5))
down_limit=int(4*(h/5))

print("Red line y:",str(line_down))
print("Blue line y:",str(line_up))
line_down_color=(255,0,0)
line_up_color=(255,0,255)
pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#Background Subtractor
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#Kernals
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((11,11),np.uint8)


font = cv2.FONT_HERSHEY_SIMPLEX
cars = []
max_p_age = 5
pid = 1


while(cap.isOpened()):
    ret,frame=cap.read()
    for i in cars:
        i.age_one()
    fgmask=fgbg.apply(frame)
    fgmask2=fgbg.apply(frame)

    if ret==True:

        #Binarization
        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2=cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
        #OPening i.e First Erode the dilate
        mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)
        mask2=cv2.morphologyEx(imBin2,cv2.MORPH_CLOSE,kernalOp)

        #Closing i.e First Dilate then Erode
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)
        mask2=cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernalCl)


        #Find Contours
        countours0,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in countours0:
            area=cv2.contourArea(cnt)
            # print(area)
            if area>areaTH:
                ####Tracking######
                m=cv2.moments(cnt)
                cx=int(m['m10']/m['m00'])
                cy=int(m['m01']/m['m00'])
                x,y,w,h=cv2.boundingRect(cnt)                                                       #得到最小正矩形的各项参数，x，y为矩形左上角的坐标

                new = True
                if cy in range(up_limit,down_limit):
                    for i in cars:
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:                       #当前块的左上角点减去上一帧质心 是否小于当前最小矩形宽高
                            new = False                                                             #如果是，则不是新的块，记为False
                            i.updateCoords(cx, cy)                                                  #更新该车辆块的质心到当前

                            if i.going_UP(line_down,line_up)==True:                                 #判断是否向上行驶，并过计数线上，若反馈为真，则统计一次向上的计数
                                cnt_up+=1                                                           #统计向上车辆数+1
                                print("ID:",i.getId(),'crossed going up at', time.strftime("%c"))   #控制台打印出该车辆的行驶信息

                            elif i.going_DOWN(line_down,line_up)==True:                             #判断是否向下行驶，并过计数线下，若反馈为真，则统计一次向下的计数
                                cnt_down+=1                                                         #统计向下车辆数+1
                                print("ID:", i.getId(), 'crossed going up at', time.strftime("%c")) #控制台打印出该车辆的行驶信息
                            break                                                                   #因为不是新的块，执行完成后break退出当前i，进行下一个i的操作；
                                                                                                    # 知识点：break是跳出目前这一层的for循环，且break语句对if-else的条件语句不起作用

                        if i.getState()=='1':                                                       #vehicles.py反馈i.state的状态，默认为零，若被统计过则为1；意味着不满足上述的一些条件，
                                                                                                    #或者不是新块且被统计过，或者是新块但轨迹还没被统计过两次
                            if i.getDir()=='down'and i.getY()>down_limit:                           #如果方向向下，且过了最下的线
                                i.setDone()                                                         #则该车辆信息在vehicles中的self.done置为真
                            elif i.getDir()=='up'and i.getY()<up_limit:                             #如果方向向上，且过了最上的线
                                i.setDone()                                                         #则该车辆信息在vehicles中的self.done置为真

                        if i.timedOut():                                                            #判断车辆信息在vehicles中的self.done的值
                            index=cars.index(i)                                                     #获取i在cars中的位置值
                            cars.pop(index)                                                         #将该值踢出cars
                            del i                                                                   #删除该变量

                    if new == True: #If nothing is detected,create new                              #判断如果是新的块
                        p=vehicles.Car(pid,cx,cy,max_p_age)                                         #得到该新的块的信息放入p；pid其实是出现过的块的数量总计
                        cars.append(p)                                                              #数据添加到cars当中
                        pid+=1                                                                      #块的计数+1

                cv2.circle(frame,(cx,cy),5,(0,0,255),-1)                                            #对大于规定面积的块，标记质心
                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)                                #对大于规定面积的块，画出最小的正矩形

        for i in cars:                                                                              #对所有出现的车辆信息显示id文字信息
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)


        str_up='UP: '+str(cnt_up)
        str_down='DOWN: '+str(cnt_down)

        frame=cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        frame=cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow('Frame',frame)

        if cv2.waitKey(2)&0xff==ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
