# 角度,y軸制御test
# 赤線に対してある程度傾けて置く

import cv2
import math
import numpy as np
import time
# import socket

"""
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
"""

def threshold(image_path):
    # 画像を読み込む
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # BGRからHSVに変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 赤色の範囲を定義（赤色は2つの範囲をカバーするため、2つのマスクを作成）
    lower_red = np.array([0, 100, 100])  # ここを調整して範囲を絞ります
    upper_red = np.array([10, 255, 255])  # ここを調整して範囲を絞ります
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # 赤色のマスクを作成
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # マスクを適用して赤い部分を抽出
    result = cv2.bitwise_and(image, image, mask=mask)

    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

    return binary_image


def remove_noise(binary_image, cell_size=6, threshold=0.7):
    height, width = binary_image.shape[:2]
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cell = binary_image[y:y+cell_size, x:x+cell_size]
            red_pixels = np.sum(cell == 255)
            total_pixels = cell.size
            red_ratio = red_pixels / total_pixels
            
            if red_ratio < threshold:
                binary_image[y:y+cell_size, x:x+cell_size] = 0

    return binary_image


def center_leastSquare(binary_image):
    moments = cv2.moments(binary_image)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = None, None

    y_coords, x_coords = np.where(binary_image == 255)
    if len(x_coords) > 0:
        grouped_y_coords = []
        grouped_x_coords = []

        step = 20
        for y in range(0, max(y_coords) + step, step):
            mask = (y_coords >= y) & (y_coords < y + step)
            if np.any(mask):
                avg_y = np.mean(y_coords[mask])
                avg_x = np.mean(x_coords[mask])
                grouped_y_coords.append(avg_y)
                grouped_x_coords.append(avg_x)

        A = np.vstack([grouped_x_coords, np.ones(len(grouped_x_coords))]).T
        m, _ = np.linalg.lstsq(A, grouped_y_coords, rcond=None)[0]
        m = -m
        # デバッグ用のプリント文
        print("(m):", m)
        return cx, cy, m
    return cx, cy, None


def process_image(image_path):
    global m, binary_image
    # 赤色のピクセルを抽出して2値化
    binary_image = threshold(image_path)
    # 画像のノイズを消す
    denoised_image = remove_noise(binary_image)
    # 最小二乗法で直線フィット
    cx, cy, m = center_leastSquare(denoised_image)
    
    if (m is not None):
        print(f"Fitted line: y = {m}x")
        tan_theta = 1 / m
        radians_error = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
        angle_error = np.degrees(radians_error)   # ラジアンを度に変換
        angle_error = int(angle_error)
        angle_error = -angle_error
        print("angle_error", angle_error)
        """
        if(angle_error < 0):
            move("ccw", -angle_error)
        else:
            move("cw", angle_error)
        time.sleep(5)
        y = 100 - 100 * math.cos(radians_error)
        y = int(y)
        move("forward", y)
        time.sleep(3)
        """

# グローバル変数
cx, cy = None, None
m = None
binary_image = None
image_path = r'C:\Users\daiko\drone\img\redLine_test\redLine150_1.jpg'

"""
# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
time.sleep(8)
"""

# 画像処理
process_image(image_path)

"""
# 着陸
send("land")
receive()

# ソケットを閉じる
sock.close()
"""