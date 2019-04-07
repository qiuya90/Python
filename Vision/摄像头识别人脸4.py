# -*- coding: utf-8 -*-
import face_recognition
import cv2
import socket
import datetime   #导入时间模块
import threading
import time
import inspect
import ctypes
import os
import 弹窗获取输入文本

video_capture = cv2.VideoCapture(0)

# 获取训练好的人脸的参数数据，这里直接从GitHub上使用默认值
face_cascade = cv2.CascadeClassifier('D:/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_64/Lib/'
                                     'site-packages/cv2/data/haarcascade_frontalface_default.xml')

faces_encoding = []
faces_name = []


def FaceEncoding():
    for root, dirs, files in os.walk('./pics/'):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                path = os.path.join(root, file)
                name = os.path.splitext(file)[0]
                faces_name.append(name)
                fileName_img = name + "_img"
                fileName_img = face_recognition.load_image_file(path)
                fileName_encoding = name + "_face_encoding"
                fileName_encoding = face_recognition.face_encodings(fileName_img, num_jitters=2)[0]
                faces_encoding.append(fileName_encoding)
    # print(faces_encoding)


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
strOn = 'http://192.168.1.5/LightOn\r\n'
strOff = 'http://192.168.1.5/LightOff\r\n'
i = 0
k = 0
LightState = False
WindowState = True

threads = []

def LightControl(command):
    # 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('192.168.1.5', 8080))
    s.send(command.encode())
    # 关闭连接:
    s.shutdown(2)
    s.close()

def FaceRecog(process_this_frame):
    global i,k,LightState
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        if process_this_frame:
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                match = face_recognition.compare_faces(faces_encoding, face_encoding, tolerance=0.39)
                for n in range(len(faces_name)):
                    if match[n]:
                        name = faces_name[n]
                        i += 1
                        k = 0
                    # elif match[1]:
                    #     name = faces_name[1]
                    #     i += 1
                    #     k = 0
                    else:
                        name = "unknown"
                    face_names.append(name)       #将结果显示在画面上

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),  2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

        if i >= 10 and (LightState is False):
            LightControl(strOn)
            i = 0
            LightState = True
            t = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')  # 获得当前系统时间
            cv2.imwrite("./pic/" + t + ".jpg", frame)
            print(video_capture.get(3))  # 得到长宽
            print(video_capture.get(4))
            print("success to record" + str(t) + ".jpg")
            print("-------------------------")

        k += 1
        if k >= 200 and (LightState is True):
            LightControl(strOff)
            k = 0
            LightState = False
        elif k >= 1000:
            k = 0

        cv2.imshow('Face_Recognition', frame)

def _async_raise(tid, exctype):
   """raises the exception, performs cleanup if needed"""
   tid = ctypes.c_long(tid)
   if not inspect.isclass(exctype):
      exctype = type(exctype)
   res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
   if res == 0:
      raise ValueError("invalid thread id")
   elif res != 1:
      # """if it returns a number greater than one, you're in trouble,
      # and you should call it again with exc=NULL to revert the effect"""
      ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
      raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
   _async_raise(thread.ident, SystemExit)


if __name__=="__main__":
    while True:
        keypress = cv2.waitKey(1)
        if WindowState is True:
            ret, frame = video_capture.read()
            cv2.imshow('Face_Recognition', frame)
            if keypress & 0xFF == ord('i'):  # 若检测到按键 ‘i’，打印字符串
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 探测图片中的人脸
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.15,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.cv2.CASCADE_SCALE_IMAGE
                )
                if len(faces) != 0:
                    name = 弹窗获取输入文本.main_window()
                    if len(name) != 0:
                        cv2.imwrite("./pics/" + name + ".jpg", frame)
                        print(video_capture.get(3))  # 得到长宽
                        print(video_capture.get(4))
                        print("success to save " + str(name) + ".jpg")
                        print("-------------------------")

        if keypress & 0xFF == ord('e'):
            thread2 = threading.Thread(target=FaceEncoding())
            thread2.setDaemon(True)
            thread2.start()
            print("Encoding success!!!")

        if keypress & 0xFF == ord('r'):
            if WindowState is True:
                WindowState = False
                thread1 = threading.Thread(target=FaceRecog, args=(process_this_frame,))
                thread1.setDaemon(True)
                thread1.start()

        if keypress & 0xFF == ord('s'):
            if WindowState is False:
                if thread1.is_alive() is True:
                    WindowState = True
                    time.sleep(0.2)
                    stop_thread(thread1)

        if keypress & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
