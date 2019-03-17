# 识别图片中的人脸
import face_recognition
weilai_image = face_recognition.load_image_file('./pic/weilai3.jpg')
ivan_image = face_recognition.load_image_file('./pic/ivan.jpg')
unknown_image = face_recognition.load_image_file('./pic/weilai2.jpg')

weilai_encoding = face_recognition.face_encodings(weilai_image)[0]
ivan_encoding = face_recognition.face_encodings(ivan_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([weilai_encoding, ivan_encoding], unknown_encoding)
labels = ['weilai', 'ivan']

print('results:'+str(results))

for i in range(0, len(results)):
    if results[i] == True:
        print('The person is:'+labels[i])