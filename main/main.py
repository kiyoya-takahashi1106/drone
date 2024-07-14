print("python script!!!!!")
# library
import cv2
import socket
import sys
import time
import numpy as np

# module
from capture_image import capture_image
from binarization import binarization
from remove_noise import remove_noise
from group_coordinates import group_coordinates
from remove_isolated_points import remove_isolated_points
from center_leastSquare import center_leastSquare
from control import control


# 定数の初期化
# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
STREAM_URL = 'udp://0.0.0.0:11111'
# パラメーター入力
N = sys.argv[1]
M = sys.argv[2]
Move_lenght_y = sys.argv[3]
Move_lenght_x = sys.argv[4]
N, M, Move_lenght_y, Move_lenght_x = int(N), int(M), int(Move_lenght_y), int(Move_lenght_x)
print("(N, M, Move_lenght_y, Move_lenght_x)", N, M, Move_lenght_y, Move_lenght_x)
# 定数初期化
Cell_size = 6
Threshold = 0.7
Step = 20
Radius = 40


# Drone設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))
selected_port = sock.getsockname()[1]
print(f"Selected port: {selected_port}")

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

# バッテリー残量を確認
send("battery?")
battery = receive()
print("battery", battery)
# if(battery < 30):
#   print("充電してください")

# カメラ設定
send("streamon")
receive()
time.sleep(2)

# OpenCVを使ってストリームを取得
cap = cv2.VideoCapture(STREAM_URL)


# 制御計算(x軸制御した後, 角度&y軸制御)
def calculate_control1():
    # 写真を撮る
    image_path = capture_image()
    image = cv2.imread(image_path)
    # x軸制御
    binary_image = binarization(image)
    denoised_image = remove_noise(binary_image, Cell_size, Threshold)
    y_coords, x_coords = np.where(denoised_image == 255)
    grouped_x_coords, grouped_y_coords = group_coordinates(x_coords, y_coords, Step)
    filtered_x_coords, filtered_y_coords = remove_isolated_points(grouped_x_coords, grouped_y_coords, Radius)
    cx, cy, m = center_leastSquare(filtered_x_coords, filtered_y_coords)
    _, _, x_error = control(prevDistance, 960, 720, cx, cy, m)
    return x_error

def calculate_control2():
    # 写真を撮る
    image_path = capture_image()
    image = cv2.imread(image_path)
    # 角度, y軸制御
    binary_image = binarization(image)
    denoised_image = remove_noise(binary_image, Cell_size, Threshold)
    y_coords, x_coords = np.where(denoised_image == 255)
    grouped_x_coords, grouped_y_coords = group_coordinates(x_coords, y_coords, Step)
    filtered_x_coords, filtered_y_coords = remove_isolated_points(grouped_x_coords, grouped_y_coords, Radius)
    cx, cy, m = center_leastSquare(filtered_x_coords, filtered_y_coords)
    angle_error, y_error, _ = control(prevDistance, 960, 720, cx, cy, m)
    return angle_error, y_error


# 動作
send("command")
receive()

send("takeoff")
time.sleep(5)  # 離陸の安定時間

# パラメーター初期化
i = 0
if(M % 2) == 0:
    L = M // 2 
else:
    L = M // 2 + 1
copy_M = M   # 残り何行あるか
move_flag = False   # ラスト1行になったらTrue
angle_error_flag = False   # Trueなら角度誤差を修正
y_error_flag = False   # Trueならy軸誤差を修正
x_error_flag = False   # Trueならx軸誤差を修正
sum_y_error = 0
prevDistance = 0

while(i < L):   
    j = 0
    while(j < N + 2):
        # x軸関係
        if(j != 0): 
            # x軸制御計算
            x_error = calculate_control1()
            # x軸制御設定
            if(x_error < -15  or  15 < x_error):   # ☆値は要調整☆
                x_error_flag = True
            if(j < N):
                if(x_error_flag == True):
                    x = x_error
                    x_error_flag = False
                else:
                    x = 0
            elif(N <= j < N+2):
                if(x_error_flag == True):
                    x = -x_error
                    x_error_flag = False
                else:
                    x = 0
                    
        # j = 0 時の初期x
        else:
            x = 0
        
        # drone動作
        # x軸制御
        if(j < N):  
            # x軸制御
            if(x == 0):
                pass
            else:
                if(x < 0):
                    x = -x
                    move("left", x)
                elif(0 < x):
                    move("right", x)
                time.sleep(4)
        
        
        
        # 角度,y軸制御, droneマニュアル動作関係
        if(j != 0): 
            # 角度,y軸制御計算
            angle_error, y_error = calculate_control2()
            # 角度制御設定 
            if(angle_error <= -10  or  10 <= angle_error):   # ☆値は要調整☆
                angle_error_flag = True
            if(j < N):
                if(angle_error_flag == True):
                    if(move_flag == False):   # angle_errorが-45° ~ 45°の間だけ想定. それ以外ならバグる
                        angle = 45 - angle_error
                    else:
                        angle = 45 + angle_error
                    angle_error_flag = False
                else:
                    angle = 45
            elif(N <= j < N+2):
                if(angle_error_flag == True):
                    angle = angle_error
                    angle_error_flag = False
                else:
                    angle = 0

            # y軸制御設定
            if(j < N):
                sum_y_error += y_error
            elif(N <= j < N+2):
                if(N == j):
                    first_half_y_error = sum_y_error   # j < Nの範囲の誤差を取り入れてマニュアル(137行目)の動く量を決める
                    sum_y_error = 0
                sum_y_error += y_error
            if(sum_y_error <= -20  or  20 <= sum_y_error):   # ☆☆値は要調整☆☆
                y_error_flag = True
            if(j < N):
                if(y_error_flag == True):
                    y = Move_lenght_y + sum_y_error
                    y_error_flag = False
                    sum_y_error = 0
                else:
                    y = Move_lenght_y
            elif(N <= j < N+2):
                if(j == N+1):
                    if(y_error_flag == True):
                        y = (Move_lenght_y*(N-1) - first_half_y_error) // 2 + sum_y_error   
                        y_error_flag = False
                        sum_y_error = 0
                else:   # j == Nの時は確定でこっち
                    y = (Move_lenght_y*(N-1) - first_half_y_error) // 2
            prevDistance = y
        
        # j = 0 時の初期angleとy
        else:
            angle = 45
            y = 90
            prevDistance = y
            
        # drone動作
        # 角度,y軸制御
        if(j < N): 
            # マニュアル動作 (左右に首振って前進をN回繰り返す. 列数がラスト1ならば右に首振るだけ(左には降らない))
            if(move_flag == False):   # 通常モード
                move("ccw", angle)   # 角度制御
                time.sleep(4)
                move("cw", 90)
                time.sleep(5)
                move("ccw", 45)
                time.sleep(3)
            else:   # ラスト一行
                move("cw", angle)   # 角度制御
                time.sleep(4)
                move("ccw", 45)
                time.sleep(3)
            if(j != N-1):
                move("forward", y)   # y軸制御
                time.sleep(5)
            else:
                pass
        
        # 前に戻ってくる(back方向に進む), 制御は2回目戻る時だけ(1回目はしない)
        elif(N <= j < N+2):
            if(N == j):   # 初めは180°回転
                move("ccw", 180)
                time.sleep(6)

            # 角度 & x軸制御
            elif(N == j+1):
                # 角度制御
                if(angle == 0):
                    pass
                else:
                    if(angle < 0):
                        angle = -angle
                        move("ccw", angle)
                    elif(0 < angle):
                        move("cw", angle)
                    time.sleep(3)
                
                # x軸制御
                if(x == 0):
                    pass
                else:
                    if(x < 0):
                        x = -x
                        move("right", x)
                    elif(0 < x):
                        move("left", x)
                    time.sleep(4)

            # ナチュラル動作
            move("forward", y)   # y軸制御
            time.sleep(8)
            
        j += 1
    copy_M -= 2   # 残り何行あるか更新

    # 90°半時計, まっすぐ, 90°半時計(要するに横移動) ※まっすぐ移動前に角度,x軸(90°傾いてなかったらy軸)制御
    move("ccw", 90)
    time.sleep(4)

    # x軸制御計算
    x_error = calculate_control1()
    # x軸制御(実際はy制御)
    x = x_error
    if(x < 0):
        x = -x
        move("left", x)
        sum_y_error = 0
    elif(0 < x):
        move("right", x)
        sum_y_error = 0
    time.sleep(3)
    
    # 角度制御計算
    angle_error, y_error = calculate_control1()
    # 角度制御
    angle = angle_error
    if(angle < 0):
        angle = -angle
        move("ccw", angle)
    elif(0 < angle):
        move("cw", angle)
    time.sleep(3)

    # マニュアル動作
    if(copy_M >= 2):   
        move("forward", Move_lenght_x * 2)
        time.sleep(8)
    elif(copy_M == 1): 
        move_flag = True  
        move("forward", Move_lenght_x)
        time.sleep(6)
    move("ccw", 90)
    time.sleep(5)
    i += 1

# 着陸
send("land")
receive()

# ストリームを停止
send("streamoff")
receive()

# OpenCVを終了
cap.release()
cv2.destroyAllWindows()

# ソケットを閉じる
sock.close()