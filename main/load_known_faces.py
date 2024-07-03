import face_recognition
import pathlib

def load_known_faces():
    paths = list(pathlib.Path('../img').glob('*.jpg'))
    known_face_encodings = []
    known_face_names = []

    for _ in paths:
        path = str(_)
        path_last = _.name
        ww_image = face_recognition.load_image_file(path)
        ww_face_encoding = face_recognition.face_encodings(ww_image)[0]
        known_face_encodings.append(ww_face_encoding)
        known_face_names.append(path_last[:-4])

    return known_face_encodings, known_face_names
