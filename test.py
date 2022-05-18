import numpy as np
import cv2 
from matplotlib import pyplot
import matplotlib.animation as animation
# from deepface import DeepFace

haar_cascade_face = cv2.CascadeClassifier('haarcascades\\haarcascade_frontalface_alt2.xml')

def detect_faces(cascade, test_image, scaleFactor = 1.1):
    # create a copy of the image to prevent any changes to the original one.
    image_copy = test_image.copy()
    
    #convert the test image to gray scale as opencv face detector expects gray images
    gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    
    # Applying the haar classifier to detect faces
    faces_rect = cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)
    
    for (x, y, w, h) in faces_rect:
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 5)
        
    return image_copy

cam = cv2.VideoCapture(0)

fig = pyplot.figure()
plt = fig.add_subplot(1,1,1)

while True:
    check, img_raw = cam.read()
    img_raw = cv2.flip(img_raw, 1)

    img_faces = detect_faces(haar_cascade_face, img_raw)
    img_rgb = cv2.cvtColor(img_faces, cv2.COLOR_BGR2RGB)

    cv2.imshow('Cam', img_faces)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()