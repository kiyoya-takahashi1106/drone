# 机の横幅が長くなく,3回の写真でその机に座ってる全員映る前提
# 充電量から飛ぶか決める機能つける
# library
from djitellopy import Tello
import time

# module


# 定数の初期化
tello = Tello()
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

# Telloの初期設定
tello.connect()
time.sleep(3)
"""
battery = tello.get_battery()
if(battery < 30):
    print("充電してください")
"""

# 動作
tello.takeoff()
time.sleep(5)  # 離陸の安定時間

i = 0
if(M % 3) == 0:
    L = M // 2 
else:
    L = M // 2 + 1
copy_M = M   # 残り何行あるか
move_flag = False   # ラスト1行になったらTrue

while(i < L):   
    j = 0
    while(j < N + 2):
        if(j<N):   # 写真撮りながら, 前進む
            move_commands["clockwise"](45)
            time.sleep(3)
            move_commands["counter_clockwise"](90)
            time.sleep(5)
            move_commands["clockwise"](45)
            time.sleep(3)
            move_commands["forward"](move_lenght_y)
            time.sleep(5)
        elif(N <= j):   # ただ戻ってくるだけ
            if(N == j):
                move_commands["counter_clockwise"](90)
                time.sleep(8)
            move_commands["forward"](move_lenght_y*N / 2)
            time.sleep(8)
        j += 1

    copy_M -= 2   # 残り何行あるか更新
    # 90°半時計, まっすぐ, 90°半時計(要するに横移動)
    move_commands["counter_clockwise"](90)
    time.sleep(5)
    if(copy_M >= 2):   
        move_commands["forward"](move_lenght_x * 2)
        time.sleep(6)
    elif(copy_M == 1): 
        move_flag = True  
        move_commands["forward"](move_lenght_x)
        time.sleep(6)
    move_commands["counter_clockwise"](90)
    time.sleep(5)
    i += 1

tello.land()
time.sleep(5)  # 着陸の安定時間

# Telloの接続切
tello.end()