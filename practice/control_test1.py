# 角度制御test
# 赤線に対してある程度傾けて置く

import cv2
import numpy as np
import threading
import socket
import time


# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# UDPソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9001))

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


def threshold(image_path):
    # 画像を読み込む
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # BGRからHSVに変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 赤色の範囲を定義（赤色は2つの範囲をカバーするため、2つのマスクを作成）
    lower_red1 = np.array([0, 50, 50], dtype=np.uint8)
    upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
    lower_red2 = np.array([170, 50, 50], dtype=np.uint8)
    upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

    # 赤色のマスクを作成
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # マスクを適用して赤い部分を抽出
    result = cv2.bitwise_and(image, image, mask=mask)

    return result

def fit_line_least_squares(binary_image):
    # 白色のピクセル座標を取得
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
        m = -m
        return m, c
    return None, None

def process_image(image_path):
    global m, c, binary_image
    # 赤色のピクセルを抽出して2値化
    red_image = threshold(image_path)
    gray_image = cv2.cvtColor(red_image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

    # 最小二乗法で直線フィット
    m, c = fit_line_least_squares(binary_image)
    if m is not None and c is not None:
        print(f"Fitted line: y = {m}x")
        tan_theta = 1 / m
        radians_error = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
        angle_error = np.degrees(radians_error)   # ラジアンを度に変換
        print(angle_error)
        angle_error = int(angle_error)
        if(angle_error < 0):
            move("ccw", -angle_error)
        else:
            move("cw", angle_error)
    else:
        print("No red pixels found to fit a line")

def visualize():
    global m, c, image_path, binary_image
    while True:
        image = cv2.imread(image_path)
        if m is not None and c is not None:
            x_vals = np.array([0, image.shape[1]])
            y_vals = m * x_vals + c
            y_vals = y_vals.astype(int)
            image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
            cv2.line(image, (x_vals[0], y_vals[0]), (x_vals[1], y_vals[1]), (0, 255, 0), 2)

        cv2.imshow('Visualization', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# グローバル変数
m, c = None, None
binary_image = None
image_path = r'C:\Users\daiko\drone\img\redLine4.jpg'

# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
time.sleep(5)

# 画像処理スレッドを開始
processing_thread = threading.Thread(target=process_image, args=(image_path,))
processing_thread.start()

# 可視化スレッドを開始
visualization_thread = threading.Thread(target=visualize)
visualization_thread.start()

# スレッドの終了を待機
processing_thread.join()
visualization_thread.join()

# 着陸
send("land")
receive()

# ソケットを閉じる
sock.close()