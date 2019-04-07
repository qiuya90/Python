import cv2
import os
import numpy as np

imgs = []
cl = []
imgPath = './Actor/izrf/'
model = cv2.face.EigenFaceRecognizer_create()    #opencv3：model = cv2.face.EigenFaceRecognizer_create()     #需要装好opencv-contrib-python
dirs = os.listdir(imgPath)
for f in dirs:
    file = imgPath + f
    img = cv2.imread(file, 0)
    imgs.append(img)
    cl.append(101)

array = np.array(cl)
model.train(imgs, array)
model.save('./XML/actor_zrf.xml')
cv2.destroyAllWindows()
