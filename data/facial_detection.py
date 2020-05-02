import cv2
import os

def get_face(image):
    image = cv2.imread(image)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    for scale in range(11, 25):
        faces = faceCascade.detectMultiScale(image, scaleFactor=scale/10, minNeighbors=5,
                                         minSize=(25, 25), flags = cv2.CASCADE_SCALE_IMAGE)
        if len(faces) == 1:
            break

    x, y, w, h = faces[0]
    size = max(w, h)
    cropped = image[y:y + size, x:x + size]
    resized = cv2.resize(cropped, (32, 32))
    return resized

PATH = ""
for i in os.listdir(PATH):
    cv2.imwrite(PATH+"/"+i, get_face(i))