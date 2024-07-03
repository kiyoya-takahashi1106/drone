# library
import cv2

# module
from load_known_faces import load_known_faces
from faceRecognition import faceRecognition



video_capture = cv2.VideoCapture(0)  # Webカメラをキャプチャ
known_face_encodings, known_face_names = load_known_faces()
recognition_active = False  # 顔認識の有効化フラグ
detected_names_all = []  # これまで顔認識した人の名前を格納するリスト

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
        
    if recognition_active:
        frame, faces_num = faceRecognition(frame, known_face_encodings, known_face_names, detected_names_all)
        # 検出された顔の数を画面に表示
        cv2.putText(frame, f"Faces: {faces_num}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        faces_num = 0

    # 結果を表示する
    cv2.imshow('WebCam', frame)
        
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        recognition_active = not recognition_active

video_capture.release()
cv2.destroyAllWindows()
print(f"Names of detected individuals: {detected_names_all}")
print(f"Number of unique individuals detected: {len(detected_names_all)}")