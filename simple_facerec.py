import face_recognition
import cv2
import numpy as np
from glob import glob
from os import path

from tqdm import tqdm

class SimpleFacerec:
    def __init__(self):
        self.known_people = []

        # key = Name, val = List of encodings/files
        self.known_face_encodings = {}
        self.known_face_files = {}

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, database_path):
        """
        Load encoding images from path
        :param database_path:
        :return:
        """
        # Load Images
        people_path = glob(path.join(database_path, '*'))
        n_images = len(glob(path.join(database_path, '*/*.*')))

        print('Loading database:')

        # Store image encoding and names
        with tqdm(total=n_images) as pbar:
            for person_path in people_path:

                name = path.basename(person_path)
                encodings = []
                files = []

                faces_path = glob(path.join(person_path, '*.png'))
                for face_path in faces_path:
                    img = cv2.imread(face_path)
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Get encoding
                    try:
                        img_encoding = face_recognition.face_encodings(rgb_img)[0]

                        # Store file name and file encoding
                        encodings.append(img_encoding)
                        files.append(face_path)
                    except IndexError:
                        pass
                    finally:
                        pbar.update()

                self.known_people.append(name)
                self.known_face_encodings.update({name: encodings})
                self.known_face_files.update({name: files})

    def save_database(self, database_path, file = 'database.npy'):
        db = np.array([self.known_people, self.known_face_files, self.known_face_encodings], dtype=object)
        np.save(path.join(database_path, file), db)

    def load_database(self, database_path, file = 'database.npy'):
        """
        Load database from path
        Returns True if loading was successful else False
        """

        db_path = path.join(database_path, file)
        if not path.exists(db_path): return False

        print('Loading database from file')

        db = np.load(db_path, allow_pickle=True)
        self.known_people = db[0]
        self.known_face_files = db[1]
        self.known_face_encodings = db[2]

        print('Done')
        return True

    def detect_known_faces(self, frame, tolerance=0.6):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        matches_people = []
        matches_filenames = []
        for face_encoding in face_encodings:
            for person in self.known_people:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings[person], face_encoding, tolerance=tolerance)

                if True in matches:
                    # # If a match was found in known_face_encodings, just use the first one.
                    # first_match_index = matches.index(True)
                    # filename = self.known_face_filenames[person][first_match_index]
                    # matches_filenames.append(filename)

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings[person], face_encoding)
                    best_match_index = np.argmin(face_distances)
                    filename = self.known_face_files[person][best_match_index]
                    matches_filenames.append(filename)

                    matches_people.append(person)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), matches_filenames, matches_people