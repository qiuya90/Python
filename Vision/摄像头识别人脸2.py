# -*- coding: utf-8 -*-
import face_recognition
import cv2
import socket
import datetime   #导入时间模块
import threading
import time
import inspect
import ctypes

video_capture = cv2.VideoCapture(0)

weilai_img = face_recognition.load_image_file('./pic/weilai3.jpg')
weilai_face_encoding = face_recognition.face_encodings(weilai_img, num_jitters=10)[0]
ivan_img = face_recognition.load_image_file('./pic/ivan1.jpg')
ivan_face_encoding = face_recognition.face_encodings(ivan_img, num_jitters=10)[0]

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
                match = face_recognition.compare_faces([weilai_face_encoding, ivan_face_encoding], face_encoding, tolerance=0.39)

                if match[0]:
                    name = "Weilai"
                elif match[1]:
                    name = "Ivan"
                    i += 1
                    k = 0
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
            print("success to save" + str(t) + ".jpg")
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
        if WindowState is True:
            ret, frame = video_capture.read()
            cv2.imshow('Face_Recognition', frame)

        keypress = cv2.waitKey(1)
        if keypress & 0xFF == ord('r'):
            WindowState = False
            thread1 = threading.Thread(target=FaceRecog, args=(process_this_frame,))
            thread1.setDaemon(True)
            thread1.start()

        if keypress & 0xFF == ord('s'):
            WindowState = True
            time.sleep(0.2)
            stop_thread(thread1)

        if keypress & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
