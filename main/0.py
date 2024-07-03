import socket
import time
import cv2
import numpy as np
import av
import threading
import pathlib
from insightface.app import FaceAnalysis
import warnings

# Telloの設定
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
LOCAL_PORT = 9001  # 使用されていない別のポートに変更
VIDEO_PORT = 11112

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_PORT))

# albumentationsのバージョンチェック警告を無視する
warnings.filterwarnings("ignore", category=UserWarning, module='albumentations')

def send(message):
    try:
        sock.sendto(message.encode(), TELLO_ADDRESS)
        print(f"Sending message: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

def receive():
    try:
        response, _ = sock.recvfrom(1024)
        print(f"Received message: {response.decode()}")
    except UnicodeDecodeError:
        print("Received message: (unable to decode)")
    except Exception as e:
        print(f"Error receiving message: {e}")

# スレッド終了用のイベントフラグ
stop_event = threading.Event()
recognition_active = threading.Event()

# InsightFaceの設定
app = FaceAnalysis(name='buffalo_l', root='~/.insightface', allowed_modules=['detection', 'recognition'])
app.prepare(ctx_id=0, det_size=(640, 640))

# 顔画像ファイルのパスリストを読み込む
paths = list(pathlib.Path('../img').glob('*.jpg'))

known_face_encodings = []
known_face_names = []

for _ in paths:
    path = str(_)
    path_last = _.name
    img = cv2.imread(path)
    faces = app.get(img)
    if faces:
        known_face_encodings.append(faces[0].embedding)  # 特徴量を保存
        known_face_names.append(path_last[:-4])  # ファイル名を名前として保存

print("Known face encodings:", known_face_encodings)
print("Known face names:", known_face_names)

# カメラ映像を表示する関数
def receive_video():
    detected_names_all = []  # これまで顔認識した人の名前を格納するリスト
    frame_count = 0  # フレームカウント
    faces_num = 0
    recognition_thread = None

    while not stop_event.is_set():
        try:
            container = av.open(f'udp://@0.0.0.0:{VIDEO_PORT}')
            for frame in container.decode(video=0):
                if stop_event.is_set():
                    break
                image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                
                # 画像のリサイズ
                small_image = cv2.resize(image, (0, 0), fx=0.4, fy=0.4)
                
                frame_count += 1
                
                if frame_count % 6 == 0:  # 6フレームごとに表示および顔認識
                    if recognition_active.is_set():
                        faces = app.get(small_image)
                        faces_num = len(faces)
                        for face in faces:
                            bbox = face.bbox.astype(int)
                            cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
                            if face.kps is not None:
                                for kp in face.kps:
                                    kp = kp.astype(int)
                                    cv2.circle(image, (kp[0], kp[1]), 1, (0, 255, 0), 2)
                            
                            # 既知の顔と照合
                            min_dist = float('inf')
                            name = "Unknown"
                            for known_face_encoding, known_face_name in zip(known_face_encodings, known_face_names):
                                dist = np.linalg.norm(face.embedding - known_face_encoding)
                                if dist < min_dist:
                                    min_dist = dist
                                    name = known_face_name
                            if name != "Unknown":
                                cv2.putText(image, name, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                                if name not in detected_names_all:
                                    detected_names_all.append(name)

                        # 検出された顔の数を画面に表示
                        cv2.putText(image, f"Faces: {faces_num}", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    cv2.imshow('Tello', image)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop_event.set()
                    break
                elif cv2.waitKey(1) & 0xFF == ord('r'):
                    if recognition_active.is_set():
                        recognition_active.clear()
                    else:
                        recognition_active.set()
            container.close()
        except av.error.OSError as e:
            print(f"Error receiving video stream: {e}")
            time.sleep(1)  # 再試行前に少し待機

    cv2.destroyAllWindows()
    print(f"Names of detected individuals: {detected_names_all}")
    print(f"Number of unique individuals detected: {len(detected_names_all)}")

# 別スレッドでビデオストリームを受信
video_thread = threading.Thread(target=receive_video)
video_thread.start()

# SDKモードを開始
send("command")
receive()

# カメラストリームをオンにする
send("streamon")
receive()
time.sleep(12)

time.sleep(120)
# send("takeoff")
# time.sleep(10)

# send("up 60")
# time.sleep(60)

# send("land")
# receive()

# カメラストリームをオフにする
send("streamoff")
receive()

# スレッドを停止する
stop_event.set()
video_thread.join()

# ソケットを閉じる
sock.close()

# OpenCVウィンドウを閉じる
cv2.destroyAllWindows()
