# facerecognition.py
import cv2
import numpy as np
import face_recognition

def faceRecognition(frame, known_face_encodings, known_face_names, detected_names_all):
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    detected_names = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name not in detected_names:
                detected_names.append(name)
            if name not in detected_names_all:
                detected_names_all.append(name)

        # 顔の周りに四角を描画する
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 名前ラベルを描画
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 2)
    
    faces_num = len(detected_names)
    return frame, faces_num