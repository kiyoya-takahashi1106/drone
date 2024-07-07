# 机の横幅が長くなく,3回の写真でその机に座ってる全員映る前提
# 充電量から飛ぶか決める機能つける
# library
import socket
import time

# module


# 定数の初期化
# TelloのIPアドレスとポート番号
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
N = int(input("Q:机が縦に何個置かれてますか？   A:"))
M = int(input("A:机が横に何個置かれてますか？   A:"))
move_lenght_y = int(input("Q:1回のy軸移動量を教えてください A:"))
move_lenght_x = int(input("Q:1回のx軸移動量を教えてください A:"))
move_commands = {
    "forward": tello.move_forward,
    "back": tello.move_back,
    "left": tello.move_left,
    "right": tello.move_right,
    "up": tello.move_up,
    "down": tello.move_down,
    "clockwise":  tello.rotate_clockwise,
    "counter_clockwise": tello.rotate_counter_clockwise
}


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

def move(direction, distance_angle):
    send(f"{direction} {distance_angle}")
    receive()

battery = tello.get_battery()
print("battery", battery)
"""
if(battery < 30):
    print("充電してください")
"""

# 動作
send("command")
receive()

send("takeoff")
time.sleep(3)  # 離陸の安定時間

i = 0
if(M % 2) == 0:
    L = M // 2 
else:
    L = M // 2 + 1
copy_M = M   # 残り何行あるか
move_flag = False   # ラスト1行になったらTrue

while(i < L):   
    j = 0
    while(j < N + 2):
        if(j<N):   # 写真撮りながら, 前進む
            if(move_flag == False):
                move("ccw", 45)
                time.sleep(3)
                move("cw", 90)
                time.sleep(5)
                move("ccw", 45)
                time.sleep(3)
                move("forward", move_lenght_y)
                time.sleep(5)
            else:
                move("cw", 45)
                time.sleep(3)
                move("ccw", 45)
                time.sleep(3)
                move("forward", move_lenght_y)
                time.sleep(5)
        elif(N <= j):   # ただ戻ってくるだけ
            if(N == j):
                move("ccw", 180)
                time.sleep(8)
            move("forward", move_lenght_y*N / 2)
            time.sleep(8)
        j += 1

    copy_M -= 2   # 残り何行あるか更新
    # 90°半時計, まっすぐ, 90°半時計(要するに横移動)
    move("ccw", 90)
    time.sleep(5)
    if(copy_M >= 2):   
        move("forward", move_lenght_x * 2)
        time.sleep(6)
    elif(copy_M == 1): 
        move_flag = True  
        move("forward", move_lenght_x)
        time.sleep(6)
    move("ccw", 90)
    time.sleep(5)
    i += 1

send("land")
receive()

# ソケットを閉じる
sock.close()
