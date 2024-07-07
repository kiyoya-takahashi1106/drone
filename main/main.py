# 机の横幅が長くなく,3回の写真でその机に座ってる全員映る前提
# 充電量から飛ぶか決める機能つける
# library
import socket
import time

# module
from threshold import threshold
from center_leastSquare import center_lastSquare
from control import control


# 定数の初期化
# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
N = int(input("Q:机が縦に何個置かれてますか？   A:"))
M = int(input("A:机が横に何個置かれてますか？   A:"))
Move_lenght_y = int(input("Q:1回のy軸移動量を教えてください A:"))
Move_lenght_x = int(input("Q:1回のx軸移動量を教えてください A:"))


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
"""
battery = tello.get_battery()
if(battery < 30):
    print("充電してください")
"""


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
x_error_flag = False
sum_y_error = 0
prevDistance = 0

# ストリーミング開始
tello.streamon()
frame_read = tello.get_frame_read()

while(i < L):   
    j = 0
    while(j < N + 2):
        # 制御 & パラメーター更新
        if(i != 0 or j != 0): 
            # 制御計算
            frame = frame = frame_read.frame
            binary_image = threshold(frame)
            cx, cy, m = center_lastSquare(binary_image)
            angle_error, y_error, x_error = control(prevDistance, 960, 720, cx, cy, m)

            # 角度制御設定
            if(angle_error <= -10  or  10 <= angle_error):   # ☆値は要調整☆
                angle_error_flag = True
            if(j < N):
                if(angle_error_flag == True):
                    if(move_flag == False):   # angle_errorが-45° ~ 45°の間だけ想定それ以外ならバグる
                        angle = 45 + angle_error
                    else:
                        angle = 45 + angle_error
                    angle_error_flag = False
                else:
                    angle = 45
            elif(N <= j):
                if(angle_error_flag == True):
                    angle = angle_error
                    angle_error_flag = False
                else:
                    angle = 0

            # y軸制御設定
            if(j < N):
                sum_y_error += y_error
            elif(N <= j):
                sum_y_error -= y_error
            if(sum_y_error <= -15  or  15 <= sum_y_error):   # ☆☆値は要調整☆☆
                y_error_flag = True
            if(j < N):
                if(y_error_flag == True):
                    y = Move_lenght_y + sum_y_error
                    y_error_flag = False
                    sum_y_error = 0
                else:
                    y = Move_lenght_y
            elif(N <= j):
                if(y_error_flag == True):
                    y = Move_lenght_y*N / 2 - sum_y_error
                    y_error_flag = False
                    sum_y_error = 0
                else:
                    y = Move_lenght_y*N / 2
            prevDistance = y

            # x軸制御設定
            if(x_error < -15  or  15 < x_error):
                x_error_flag = True
            if(j < N):
                if(x_error_flag == True):
                    x = x_error
                    x_error_flag = False
                else:
                    x = 0
            elif(N <= j):
                if(x_error_flag == True):
                    x = -x_error
                    x_error_flag = False
                else:
                    x = 0

        # i,j = 0,0 時の初期パラメーター
        else:
            angle = 45
            y = 90
            x = 0


        # drone動作
        # 写真撮りながら, forward方向に進む
        if(j < N):  
            # x軸制御
            if(x == 0):
                pass
            else:
                if(x < 0):
                    x = -x
                    Move_commands["left"](x)
                elif(0 < x):
                    Move_commands["right"](x)
                time.sleep(4)

            # マニュアル動作
            if(move_flag == False):   # 通常モード
                Move_commands["counter_clockwise"](angle)   # 角度制御
                time.sleep(4)
                Move_commands["clockwise"](90)
                time.sleep(5)
                Move_commands["counter_clockwise"](45)
                time.sleep(3)
                Move_commands["forward"](y)   # y軸制御
                time.sleep(5)
            else:   # ラスト一行
                Move_commands["clock_wise"](angle)   # 角度制御
                time.sleep(4)
                Move_commands["counter_clockwise"](45)
                time.sleep(3)
                Move_commands["forward"](y)   # y軸制御
                time.sleep(5)

        # 前に戻ってくる(back方向に進む)
        elif(N <= j):   
            if(N == j):   # 初めは180°回転
                Move_commands["counter_clockwise"](180)
                time.sleep(8)
            # 角度制御
            if(angle == 0):
                pass
            else:
                if(angle < 0):
                    angle = -angle
                    Move_commands["counter_clockwise"](angle)
                elif(0 < angle):
                    Move_commands["clockwise"](angle)
                time.sleep(3)

            # x軸制御
            if(x == 0):
                    pass
            else:
                if(x < 0):
                    x = -x
                    Move_commands["left"](x)
                elif(0 < x):
                    Move_commands["right"](x)
                time.sleep(4)
            
            # ナチュラル動作
            Move_commands["forward"](y)   # y軸制御
            time.sleep(8)
        j += 1

    copy_M -= 2   # 残り何行あるか更新

    # 90°半時計, まっすぐ, 90°半時計(要するに横移動) ※まっすぐ移動前に角度,x軸(90°傾いてなかったらy軸)制御
    Move_commands["counter_clockwise"](90)
    time.sleep(5)
    # 制御計算
    frame = frame = frame_read.frame
    binary_image = threshold(frame)
    cx, cy, m = center_lastSquare(binary_image)
    angle_error, _, x_error = control(prevDistance, 960, 720, cx, cy, m)
    
    # 角度制御
    angle = angle_error
    if(angle < 0):
        angle = -angle
        Move_commands["counter_clockwise"](angle)
    elif(0 < angle):
        Move_commands["clockwise"](angle)
    time.sleep(3)
    
    # x軸制御
    x = x_error
    if(x < 0):
        x = -x
        Move_commands["left"](x)
        sum_y_error = 0
    elif(0 < x):
        Move_commands["right"](x)
        sum_y_error = 0
    time.sleep(3)

    # ナチュラル動作
    if(copy_M >= 2):   
        Move_commands["forward"](Move_lenght_x * 2)
        time.sleep(8)
    elif(copy_M == 1): 
        move_flag = True  
        Move_commands["forward"](Move_lenght_x)
        time.sleep(6)
    Move_commands["counter_clockwise"](90)
    time.sleep(5)
    i += 1

tello.land()
time.sleep(5)  # 着陸の安定時間

# Telloの接続切
tello.end()