from simple_facerec import SimpleFacerec
from argparse import ArgumentParser
from matplotlib import pyplot
from pathlib import Path
import numpy as np
import cv2

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

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
    return (check, image_copy, image_face, image_face_pos)

def crm(cam: int, database: Path):
    sfr = SimpleFacerec()
    if not sfr.load_database(database):
        sfr.load_encoding_images(database)
        sfr.save_database(database)

    cam = cv2.VideoCapture(cam)

    fig = pyplot.figure()
    plt = fig.add_subplot(1,1,1)

    max_count = 10
    count = 0

    face_found = False
    current_image = None
    current_name = ""

    window = 'Celebrity Resemblance Machine'
    cv2.namedWindow(window, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:

        # Get image from webcam
        check, img_raw = cam.read()
        img_raw = cv2.flip(img_raw, 1)

        check, img, img_face, img_face_pos = detect_faces(haar_cascade_face, img_raw)
        if check:
            face_locations, face_files, face_names = sfr.detect_known_faces(img_face)
            if(len(face_names)>0):
                
                # cv2.addText(img, face_names[0], (img_face_pos[0], img_face_pos[1]+img_face_pos[3]+20), 'Comic Sans')
                pil_img = Image.fromarray(img)
                match_img = cv2.cvtColor(np.array(Image.open(face_files[0])), cv2.COLOR_RGB2BGR)
                match_img = Image.fromarray(match_img)
                match_img = match_img.resize((img_face_pos[2], img_face_pos[3]))

                if(face_found != True):
                    
                    current_name = face_names[0]

                    pil_img.paste(match_img, box=(img_face_pos[0]+img_face_pos[2]+10, img_face_pos[1]))
                    draw = ImageDraw.Draw(pil_img)
                    font = ImageFont.truetype('ComicSansMS3.ttf', 30)
                    draw.text((img_face_pos[0], img_face_pos[1]+img_face_pos[3]+10),face_names[0], (255,255,255), font=font)
                    img = np.array(pil_img)

                    current_image = match_img;

                    face_found = True;

                else:
                    
                    count = count+1;
                    pil_img.paste(current_image, box=(img_face_pos[0]+img_face_pos[2]+10, img_face_pos[1]))

                    draw = ImageDraw.Draw(pil_img)
                    font = ImageFont.truetype('ComicSansMS3.ttf', 30)
                    draw.text((img_face_pos[0], img_face_pos[1]+img_face_pos[3]+10), current_name, (255,255,255), font=font)
                    
                    img = np.array(pil_img)

                    if(count >= max_count):
                        count = 0;
                        face_found = False;

            else:
                pil_img = Image.fromarray(img)
                draw = ImageDraw.Draw(pil_img)
                font = ImageFont.truetype('ComicSansMS3.ttf', 30)
                
                if(current_image != None):
                    pil_img.paste(current_image, box=(img_face_pos[0]+img_face_pos[2]+10, img_face_pos[1]))
                
                if(current_name != None):
                    draw.text((img_face_pos[0], img_face_pos[1]+img_face_pos[3]+10), current_name, (255,255,255), font=font)
                else:
                    draw.text((img_face_pos[0], img_face_pos[1]+img_face_pos[3]+10), "Not found", (255,0,0), font=font)



                img = np.array(pil_img)
                

        cv2.imshow(window, img)

        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = ArgumentParser(prog="crm")
    parser.add_argument('cam', type=int, help='Camera ID')
    parser.add_argument('--database', type=Path, required=False, default='./Celebs', help='Database')
    args = parser.parse_args()

    print("Press 'q' to quit")
    crm(args.cam, args.database)