# auto-testとcamera,顔認識

import socket
import time
import cv2
import numpy as np
import av
import threading
import face_recognition

# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
LOCAL_PORT = 9000
VIDEO_PORT = 11111

# UDPソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_PORT))

def send(message):
    try:
        sock.sendto(message.encode(), TELLO_ADDRESS)
        print(f"Sending message: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

def receive():
    try:
        response, _ = sock.recvfrom(1024)  # response:受信データ , _:送信元アドレス
        print(f"Received message: {response.decode()}")
    except Exception as e:
        print(f"Error receiving message: {e}")

# スレッド終了用のイベントフラグ
stop_event = threading.Event()

# カスケードファイルのパスを設定
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# カメラ映像を表示し、写真を保存する関数
saved_images = []
def receive_video():
    container = av.open(f'udp://@0.0.0.0:{VIDEO_PORT}')
    frame_skip = 0  # フレームスキップ用のカウンタ
    for frame in container.decode(video=0):
        if stop_event.is_set():
            break
        image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        
        # フレームスキップ
        if frame_skip % 10 == 0:  # Xフレームごとに顔検出を行う
            # グレースケールに変換
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 顔検出
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            # 検出された顔に矩形を描画
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        frame_skip += 1
        cv2.imshow('Tello', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
    cv2.destroyAllWindows()

def save_photo(image, filename):
    cv2.imwrite(filename, image)
    saved_images.append(filename)
    print(f"Saved photo: {filename}")

# 人物認識関数
def recognize_person(image_path, known_face_encodings, known_face_names):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        print(f"Found {name} in {image_path}")

# 既知の顔データをロード（ここに事前に登録した人物の顔画像を使用）
known_face_encodings = []
known_face_names = []

# ここで登録したい人物の画像と名前を追加
# 例:
# known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file("person1.jpg"))[0])
# known_face_names.append("Person 1")

# 別スレッドでビデオストリームを受信
video_thread = threading.Thread(target=receive_video)
video_thread.start()

# SDKモードを開始
send("command")
receive()

# カメラストリームをオンにする
send("streamon")
receive()

# 離陸
send("takeoff")
time.sleep(7)

send("up 40")

once_forward = 80   # 一回でどれだけ前進するか
how_many_forward = 6   # 何回前進するか
angle = 45   # 左右に向く角度
photo_index = 1
for i in range(how_many_forward):
    time.sleep(5)
    if(i == 0):
        send(f"cw {angle}")
        time.sleep(5)
        save_photo(image, f"photo_{photo_index}.jpg")
        photo_index += 1
        send(f"ccw {angle * 2}")
        time.sleep(5)
        save_photo(image, f"photo_{photo_index}.jpg")
        photo_index += 1
        send(f"cw {angle}")
        time.sleep(5)
    send(f"forward {once_forward}")
    time.sleep(5)
    send(f"cw {angle}")
    time.sleep(5)
    save_photo(image, f"photo_{photo_index}.jpg")
    photo_index += 1
    send(f"ccw {angle * 2}")
    time.sleep(5)
    save_photo(image, f"photo_{photo_index}.jpg")
    photo_index += 1
    send(f"cw {angle}")

# 元の位置に戻る
time.sleep(14) 
if(once_forward * how_many_forward < 500 ):
    send(f"back {once_forward * how_many_forward}")
else:
    time.sleep(4)
    send(f"back {once_forward * how_many_forward / 2}")
    time.sleep(11)   # 長くとらないとダメかも
    send(f"back {once_forward * how_many_forward / 2}")

# 着陸
send("land")
receive()

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

# 撮影した写真に対して人物認識を行う
for image_path in saved_images:
    recognize_person(image_path, known_face_encodings, known_face_names)
