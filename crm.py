import numpy as np
import cv2
from matplotlib import pyplot

haar_cascade_face = cv2.CascadeClassifier('haarcascades\\haarcascade_frontalface_alt2.xml')

def detect_faces(cascade, test_image):
    # Create a copy of the image to prevent any changes to the original one.
    image_copy = test_image.copy()
    
    # Convert the test image to gray scale as opencv face detector expects gray images
    gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    
    # Applying the haar classifier to detect faces
    faces_rect = cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    
    # Closest face
    image_face = None
    image_face_pos = (0,0,0,0)

    for x, y, w, h in faces_rect:

        # Find closest face
        try:
            if w*h > image_face_pos[2]*image_face_pos[3]:
                image_face = image_copy[y:y+h, x:x+w]
                image_face_pos = (x,y,w,h)
        except AttributeError:
            image_face = image_copy[y:y+h, x:x+w]
            image_face_pos = (x,y,w,h)

        # Draw blue rectangle over all faces
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (255, 127, 0), 5)

    # Draw green rectangle over closest face
    try:
        if image_face.any():
            x, y, w, h = image_face_pos
            cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 127), 5)
    except AttributeError: pass

    check = len(faces_rect)>0
    return (check, image_copy, image_face)

cam = cv2.VideoCapture(0)

fig = pyplot.figure()
plt = fig.add_subplot(1,1,1)

while True:

    # Get image from webcam
    check, img_raw = cam.read()
    img_raw = cv2.flip(img_raw, 1)

    check, img, img_face = detect_faces(haar_cascade_face, img_raw)
    

    cv2.imshow('Cam', img)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()