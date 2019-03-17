# -*- coding: utf-8 -*-
import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

weilai_img = face_recognition.load_image_file('./pic/weilai3.jpg')
weilai_face_encoding = face_recognition.face_encodings(weilai_img, num_jitters=10)[0]
ivan_img = face_recognition.load_image_file('./pic/ivan1.jpg')
ivan_face_encoding = face_recognition.face_encodings(ivan_img, num_jitters=10)[0]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
strGreen = 'http://192.168.1.6/LightGREEN\r\n'
strSkyblue= 'http://192.168.1.6/LightSKYBLUE\r\n'


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
            else:
                name = "unknown"

            face_names.append(name)

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

    cv2.imshow('Video', frame)

    keypress = cv2.waitKey(1)
    if keypress & 0xFF == ord('q'):
       break

video_capture.release()
cv2.destroyAllWindows()
