import cv2
import numpy as np
import socket
import time

# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

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

def binarization(image_path):
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

def remove_noise(binary_image, cell_size, threshold):
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

def group_coordinates(x_coords, y_coords, step):
    grouped_y_coords = []
    grouped_x_coords = []

    for y in range(0, max(y_coords) + step, step):
        mask = (y_coords >= y) & (y_coords < y + step)
        if np.any(mask):
            avg_y = np.mean(y_coords[mask])
            avg_x = np.mean(x_coords[mask])
            grouped_y_coords.append(avg_y)
            grouped_x_coords.append(avg_x)
    
    return np.array(grouped_x_coords), np.array(grouped_y_coords)

def remove_isolated_points(grouped_x_coords, grouped_y_coords, radius):
    filtered_x_coords = []
    filtered_y_coords = []
    for i in range(len(grouped_x_coords)):
        x = grouped_x_coords[i]
        y = grouped_y_coords[i]
        # 周囲の点をチェック
        distances = np.sqrt((grouped_x_coords - x) ** 2 + (grouped_y_coords - y) ** 2)
        # 半径内に他の点があるかチェック
        if np.sum((distances < radius) & (distances > 0)) > 0:
            filtered_x_coords.append(x)
            filtered_y_coords.append(y)
    return np.array(filtered_x_coords), np.array(filtered_y_coords)

def center_leastSquare(filtered_x_coords, filtered_y_coords):
    if len(filtered_x_coords) > 0:
        # 重心を計算
        cx = np.mean(filtered_x_coords)
        cy = np.mean(filtered_y_coords)

        # 最小二乗法
        A = np.vstack([filtered_x_coords, np.ones(len(filtered_x_coords))]).T
        m, _ = np.linalg.lstsq(A, filtered_y_coords, rcond=None)[0]
        m = -m

        # デバッグ用のプリント文
        print("(m):", m)
        # print("(cx):", cx)
        # print("(cy):", cy)

        return cx, cy, m
    return None, None, None

def process_image(image_path):
    global m, binary_image
    # 赤色のピクセルを抽出して2値化
    binary_image = binarization(image_path)
    # 画像のノイズを消す
    denoised_image = remove_noise(binary_image, 6, 0.7)
    # 白いピクセルの座標を抽出
    y_coords, x_coords = np.where(denoised_image == 255)
    # 残った点をグループ化
    grouped_x_coords, grouped_y_coords = group_coordinates(x_coords, y_coords, 20)   # 数値の入力はstep数
    # 孤立した点を削除
    filtered_x_coords, filtered_y_coords = remove_isolated_points(grouped_x_coords, grouped_y_coords, 40)
    # 最小二乗法で直線フィット
    cx, cy, m = center_leastSquare(filtered_x_coords, filtered_y_coords)

    # fx = 0.001265 * np.exp(0.018237 * (720 - cy)) + 0.367068
    # fx = 0.003051 * np.exp(0.015006 * (720 - cy)) + 0.430705
    # fx = 0.005784 * np.exp(0.013606 * (720 - cy)) + 0.346111
    # fx = 0.006689 * np.exp(0.013240 * (720 - cy)) + 0.359777
    fx = 0.006912 * np.exp(0.013168 * (720 - cy)) + 0.355108
    print("(fx)", fx)

    # 重心cxと画面中心のずれ(d)
    cx_middle_error = 960//2 - cx
    print("(cx_middle_error)", cx_middle_error)

    # drone画面のx方向のずれを入れたら, y軸を基準とする実際のx方向のずれが分かる.
    x_error = -cx_middle_error * fx
    x_error = int(x_error)
    print("(x_error)", x_error)

    if x_error > 0:
        move("right", x_error)
    else:
        move("left", -x_error)
        
def capture_image():
    cap = cv2.VideoCapture('udp://0.0.0.0:11111')
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    time.sleep(2)  # ストリーミングの接続待機
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None

    ret, frame = cap.read()
    if ret:
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)
        print(f"Image captured and saved to {image_path}")
        cap.release()
        return image_path
    else:
        print("Error: Could not read frame.")
        cap.release()
        return None

# グローバル変数
cx, cy = None, None
m = None
binary_image = None

# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
receive()
time.sleep(3)

# ビデオストリーム開始
send("streamon")
receive()

# 写真を撮る
image_path = capture_image()

# 画像処理
if image_path:
    process_image(image_path)

# 着陸
send("land")
receive()

# ビデオストリーム停止
send("streamoff")
receive()

# ソケットを閉じる
sock.close()