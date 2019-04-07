import cv2
#读取视频信息。
# cap = cv2.VideoCapture("http://192.168.1.3:8080/video")  #@前为账号密码，后为ip地址
cap = cv2.VideoCapture(0)  #@前为账号密码，后为ip地址
face_xml = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #导入XML文件
while(cap.isOpened()):
    f,img = cap.read()   #读取一帧图片
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #转换为灰度图
    face = face_xml.detectMultiScale(gray,1.3,10)    #检测人脸，并返回人脸位置信息

    for (x,y,w,h) in face:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow("1",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() #释放摄像头
cv2.destroyAllWindows()#删除建立的全部窗口