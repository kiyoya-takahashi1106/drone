# 角度制御test
# 赤線に対してある程度x軸にずれるように置いとく

import cv2
import math
import numpy as np
import time
import socket

# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
STREAM_URL = 'udp://0.0.0.0:11111'

# UDPソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9000))

def send(message):
    try:
        sock.sendto(message.encode(), TELLO_ADDRESS)
        print(f"Sending message: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

def receive():
    try:
        response, _ = sock.recvfrom(1024)   # response:受信データ , _:送信元アドレス
        print(f"Received message: {response.decode()}")
    except Exception as e:
        print(f"Error receiving message: {e}")

def move(direction, distance):
    send(f"{direction} {distance}")
    receive()

# カメラ設定
send("streamon")
receive()
time.sleep(2)

# OpenCVを使ってストリームを取得
cap = cv2.VideoCapture(STREAM_URL)


# 制御関数定義
def threshold(image):
    # BGRからHSVに変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 白色の範囲を定義
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 50, 255], dtype=np.uint8)

    # 白色のマスクを作成
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # マスクを適用して白い部分を抽出
    result = cv2.bitwise_and(image, image, mask=mask)

    # グレースケールに変換して二値化
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    return binary


def center_lastSquare(binary_image):
    # 重心計算
    moments = cv2.moments(binary_image)   # モーメントを計算
    if moments["m00"] != 0:   # 重心が存在するか確認
        cx = int(moments["m10"] / moments["m00"])   # 重心のX座標を計算
        cy = int(moments["m01"] / moments["m00"])   # 重心のY座標を計算
    else:
        cx, cy = None, None   # 重心が存在しない場合
    

    # 最小二乗法
    # 白色のピクセル座標を取得(y,x_coordsは配列)
    y_coords, x_coords = np.where(binary_image == 255)  # 白色のピクセル座標を取得
    print("y_coords", y_coords)
    print("x_coords", x_coords)

    if len(x_coords) > 0:  # 座標が存在するか確認
        # y座標をstepピクセルごとにグループ化してx座標の平均を計算
        grouped_y_coords = []
        grouped_x_coords = []
        
        step = 50
        for y in range(0, max(y_coords) + step, step):
            mask = (y_coords >= y) & (y_coords < y + step)
            if np.any(mask):
                avg_y = np.mean(y_coords[mask])
                avg_x = np.mean(x_coords[mask])
                grouped_y_coords.append(avg_y)
                grouped_x_coords.append(avg_x)
        print("grouped_y_coords", grouped_y_coords)
        print("grouped_x_coords", grouped_x_coords)

        A = np.vstack([grouped_x_coords, np.ones(len(grouped_x_coords))]).T   # 行列を作成
        m, c = np.linalg.lstsq(A, grouped_y_coords, rcond=None)[0]   # 最小二乗法で直線をフィット(mx + c)
        return cx, cy, m
    return cx, cy, None   # 座標が存在しない場合


def control(prevDistance, img_width, img_height, cx, cy, m):   # 一つ前の行動の進んだ距離, 重心x座標, 重心y座標, 画像の幅, 画像の高さ, 傾き
    # 今の角度から垂直にする角度
    tan_theta = 1 / m
    radians_error = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
    angle_error = np.degrees(radians_error)   # ラジアンを度に変換

    # y方向のずれ
    y_error = prevDistance - prevDistance * math.cos(radians_error)

    # x方向のずれ
    # こっち側から重心までのy(img_height - cy)を入れたら, real/droの画面 比率が分かる.
    fx = (40 * (1 + np.exp(0.85 * (img_height - cy - 5.4)))) / 3.07

    # 重心cxと画面中心のずれ(d)
    cx_middle_error = img_width//2 - cx

    # drone画面のx方向のずれを入れたら, y軸を基準とする実際のx方向のずれが分かる.
    x_error = cx_middle_error * fx

    return angle_error, y_error, x_error


# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
time.sleep(5)

_, frame = cap.read()
cv2.imshow('Captured Frame', frame)
cv2.waitKey('q')  # キー入力を待つ
cv2.destroyAllWindows()

binary_image = threshold(frame)
cx, cy, m = center_lastSquare(binary_image)
_, _, x_error = control(30, 960, 720, cx, cy, m)
x = x_error

# x軸制御
if(x < 0):
    x = -x
    move("left", x)
    print(f"left {x}")
elif(x <= 0):
    move("right", x)
    print(f"right {x}")

# 着陸
send("land")
receive()

# ソケットを閉じる
sock.close()