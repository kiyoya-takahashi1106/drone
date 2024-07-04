# 机の横幅が長くなく,3回の写真でその机に座ってる全員映る前提
# 充電量から飛ぶか決める機能つける
# library
from djitellopy import Tello

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
battery = tello.get_battery()
"""
if(battery < 30):
    print("充電してください")
"""

# 動作
tello.takeoff()

i = 0
if(N % 2 == 0):
    L = N//2
else:  
    L = N//2 + 1
copy_N = N
while(i < M):   
    j = 0
    if(i%2 == 0):
        direction = "forward"
    else:
        direction = "back"
    while(j < N): 
        move_commands["clockwise"](45)
        move_commands["counter_clockwise"](90)
        move_commands["clockwise"](45)
        move_commands[direction](move_lenght_y)
        j += 1
    copy_N -= 2
    if(copy_N >= 2):   
        move_commands["left"](move_lenght_x*2)
    elif(copy_N == 1):   
        move_commands["left"](move_lenght_x)
    i += 1

tello.land()

# Telloの接続切
tello.end()