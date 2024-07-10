# x軸制御test
# 赤線に対してある程度傾けて置く

import cv2
import numpy as np
import socket
import time

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


def center_leastSquare(binary_image):
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
        # print("grouped_y_coords", grouped_y_coords)
        # print("grouped_x_coords", grouped_x_coords)

        A = np.vstack([grouped_x_coords, np.ones(len(grouped_x_coords))]).T   # 行列を作成
        m, _ = np.linalg.lstsq(A, grouped_y_coords, rcond=None)[0]   # 最小二乗法で直線をフィット(mx + _)
        m = -m
        return cx, cy, m
    return cx, cy, None   # 座標が存在しない場合


def process_image(image_path):
    global m, binary_image
    # 赤色のピクセルを抽出して2値化
    binary_image = threshold(image_path)
    cx, cy, m = center_leastSquare(binary_image)
    print("cx, cy", cx, cy)
    # print("m", m)

    # fx = 0.001265 * np.exp(0.018237 * (720 - cy)) + 0.367068
    # fx = 0.003051 * np.exp(0.015006 * (720 - cy)) + 0.430705
    # fx = 0.005784 * np.exp(0.013606 * (720 - cy)) + 0.346111
    fx = 0.006689 * np.exp(0.013240 * (720 - cy)) + 0.359777
    print("fx", fx)

    # 重心cxと画面中心のずれ(d)
    cx_middle_error = 960//2 - cx
    print("cx_middle_errir", cx_middle_error)

    # drone画面のx方向のずれを入れたら, y軸を基準とする実際のx方向のずれが分かる.
    x_error = -cx_middle_error * fx
    x_error = int(x_error)
    print("x_error", x_error)

    """
    if(0 < x_error):
        move("left", -x_error)
    else:
        move("right", x_error)
    """
        

# グローバル変数
cx, cy = None, None
m = None
binary_image = None
image_path = r'C:\Users\daiko\drone\img\redLine_test\redLine25_3.jpg'

"""
# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
time.sleep(5)
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