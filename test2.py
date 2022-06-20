import cv2 
from simple_facerec import SimpleFacerec

sfr = SimpleFacerec()
if not sfr.load_database("./DummyCelebs"):
    sfr.load_encoding_images("./DummyCelebs")
    sfr.save_database("./DummyCelebs")

cap = cv2.VideoCapture(0)   

while True:
    ret,frame = cap.read()

    face_locations, face_filenames, face_names = sfr.detect_known_faces(frame)
    # if face_names: print(face_names)
    for face_loc, filename, name in zip(face_locations, face_filenames, face_names):
        top, left, bottom, right = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (top, left -10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2)
        cv2.putText(frame, f'({filename})', (top, left+30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,200), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


