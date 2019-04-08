from random import randint

class Car:
    tracks=[]
    def __init__(self,i,xi,yi,max_age):
        self.i=i
        self.x=xi
        self.y=yi
        self.tracks=[]
        self.R=randint(0,255)
        self.G=randint(0,255)
        self.B=randint(0,255)
        self.done=False
        self.state='0'
        self.age=0
        self.max_age=max_age
        self.dir=None

    def getRGB(self):  #For the RGB colour
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks

    def getId(self): #For the ID
        return self.i

    def getState(self):
        return self.state

    def getDir(self):
        return self.dir

    def getX(self):  #for x coordinate
        return self.x

    def getY(self):  #for y coordinate
        return self.y

    def updateCoords(self, xn, yn):
        self.age = 0                                    #???重置age
        self.tracks.append([self.x, self.y])            #增加该车辆的新的质心轨迹信息
        self.x = xn                                     #更新该车辆当前质心坐标x
        self.y = yn                                     #更新该车辆当前质心坐标y

    def setDone(self):                                  #设置是否出界的值
        self.done = True

    def timedOut(self):                                 #判断是否出界的值
        return self.done

    def going_UP(self, mid_start, mid_end):                     #形参为两根计数线，计数线下、计数线上
        if len(self.tracks)>=2:                                 #跟踪轨迹需大于等于2次
            if self.state=='0':                                 #未统计过的，state默认为0,进入计数
                if self.tracks[-1][1]<mid_end and self.tracks[-2][1]>=mid_end:              #判断最后一次轨迹的y坐标小于计数线上，倒数第二次轨迹的y坐标大于计数线上，满足则向上行驶
                    state='1'                                   #一旦统计，state为1，即统计过了
                    self.dir='up'                               #判断为向上行驶，dir标记为“up”
                    return True                                 #返回真
                else:
                    return False                                #否则返回假
            else:
                return False                                    #如果统计过，state不为0，则返回假
        else:
            return False                                        #如果跟踪轨迹未统计过2次，则返回假

    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks)>=2:
            if self.state=='0':
                if self.tracks[-1][1]>mid_start and self.tracks[-2][1]<=mid_start:
                    start='1'
                    self.dir='down'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def age_one(self):
        self.age+=1                                     #将age值加1
        if self.age>self.max_age:                       #如果age值大于5，则self.done为真
            self.done=True
        return  True                                    #返回真，貌似无意义？？？

#Class2

class MultiCar:
    def __init__(self,cars,xi,yi):
        self.cars=cars
        self.x=xi
        self.y=yi
        self.tracks=[]
        self.R=randint(0,255)
        self.G=randint(0,255)
        self.B=randint(0,255)
        self.done=False
