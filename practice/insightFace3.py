# 1,2ではWebカメラに映ったものだったが, Droneのカメラに映ったものにする.

import socket
import time
import cv2
import numpy as np
import av
import threading
from insightface.app import FaceAnalysis
import os

# TelloのIPアドレスとポート設定
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
LOCAL_PORT = 9000
VIDEO_PORT = 11111

# ソケットの設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_PORT))

# メッセージ送信関数
def send(message):
    try:
        sock.sendto(message.encode(), TELLO_ADDRESS)
        print(f"Sending message: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

# メッセージ受信関数
def receive():
    try:
        response, _ = sock.recvfrom(1024)
        print(f"Received message: {response.decode()}")
    except Exception as e:
        print(f"Error receiving message: {e}")

# スレッド終了用のイベントフラグ
stop_event = threading.Event()

# 類似度の算出のための関数（コサイン類似度）
def cos_sim(feat1, feat2):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))

# 検出ボックスと名前を描画するための関数
def draw_on(img, faces, name):
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if face.kps is not None:
            kps = face.kps.astype(int)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color, 2)
        cv2.putText(dimg, name, (box[0]-1, box[1]-4), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 2)

    return dimg

# 顔検出のオブジェクトのインスタンス化
app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))

# 画像フォルダのパス
img_folder_path = 'C:\\Users\\daiko\\drone\\img'
known_face_names = []
pre_embeddings = []

# フォルダ内のすべての画像を読み込み、特徴量を抽出する
for file_name in os.listdir(img_folder_path):
    if file_name.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(img_folder_path, file_name)
        pre_img = cv2.imread(img_path)
        if pre_img is None:
            print(f"Cannot open or read the image file: {img_path}")
            continue

        pre_face = app.get(pre_img)
        if len(pre_face) == 0:
            print(f"No face detected in the image: {img_path}")
            continue

        known_face_names.append(file_name)
        pre_embeddings.append(pre_face[0].embedding)

# 顔認識を有効にするフラグ
recognition_enabled = True

# カメラ映像を表示し、顔認識を行う関数
def receive_video():
    container = av.open(f'udp://@0.0.0.0:{VIDEO_PORT}')
    for frame in container.decode(video=0):
        if stop_event.is_set():
            break
        image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)

        if recognition_enabled:
            faces = app.get(image)
            if len(faces) == 0:
                detect = image
                name = "Unknown"
            else:
                embeddings = faces[0].embedding

                best_sim = 0
                best_name = "Unknown"
                for i, pre_embedding in enumerate(pre_embeddings):
                    sim = cos_sim(pre_embedding, embeddings)
                    if sim > best_sim:
                        best_sim = sim
                        if sim >= 0.75:
                            best_name = known_face_names[i]
                        else:
                            best_name = "Unknown"

                detect = draw_on(image, faces, best_name)
        else:
            detect = image

        cv2.imshow('Tello', detect)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            stop_event.set()
            break
        elif key == ord('r'):
            global recognition_enabled
            recognition_enabled = not recognition_enabled

    cv2.destroyAllWindows()

# 別スレッドでビデオストリームを受信
video_thread = threading.Thread(target=receive_video)
video_thread.start()

# SDKモードを開始
send("command")
receive()

# カメラストリームをオンにする
send("streamon")
receive()

# 30秒間映像を表示
time.sleep(30)

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