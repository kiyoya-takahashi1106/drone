# 机の横幅が長くなく,3回の写真でその机に座ってる全員映る前提
# 充電量から飛ぶか決める機能つける
# library
import cv2
import socket
import time

# module
from threshold import threshold
from center_leastSquare import center_leastSquare
from control import control


# 定数の初期化
# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
STREAM_URL = 'udp://0.0.0.0:11111'
# パラメーター入力
N = int(input("Q:机が縦に何個置かれてますか？   A:"))
M = int(input("A:机が横に何個置かれてますか？   A:"))
Move_lenght_y = int(input("Q:1回のy軸移動量を教えてください A:"))
Move_lenght_x = int(input("Q:1回のx軸移動量を教えてください A:"))


# Drone設定
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


# 関数定義
def calculate_control():
    _, frame = cap.read()
    binary_image = threshold(frame)
    cx, cy, m = center_leastSquare(binary_image)
    angle_error, y_error, x_error = control(prevDistance, 960, 720, cx, cy, m)
    return angle_error, y_error, x_error


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

while(i < L):   
    j = 0
    while(j < N + 2):
        # 制御 & パラメーター更新
        if(j != 0): 
            # 制御計算
            angle_error, y_error, x_error = calculate_control()

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
            elif(N <= j):
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

        # j = 0 時の初期パラメーター
        else:
            angle = 45
            y = 90
            x = 0
            prevDistance = y

        # drone動作
        # 写真撮りながら, forward方向に進む
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

            # マニュアル動作 (首振って前進をN回繰り返す. 最後の一回は首振るだけ)
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
            if(N == N+1):
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

    # 制御計算
    angle_error, y_error, x_error = calculate_control()
    
    # 角度制御
    angle = angle_error
    if(angle < 0):
        angle = -angle
        move("ccw", angle)
    elif(0 < angle):
        move("cw", angle)
    time.sleep(3)
    
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

    # ナチュラル動作
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