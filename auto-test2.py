# Tello自動操縦サンプルコード2(rootを組み合わせた)

import socket
import time

TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

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

# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
time.sleep(5)

# ☆☆☆
# droneの初期位置はMap[0][0]に下向き(↓)を想定
# 今回は見せかけのMap,本来はMapを探索して最適rootを見つける
map = [
        [1, 1, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 1, 0] 
      ]
y_Distance = 70
x_Distance = 70
root = [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2], [1, 2], [1, 3], [1, 2]]   # (y, x)

for i, [y, x] in enumerate(root):   # i:idxnum
    if(i == 0):
        pass
    else:
        change_y, change_x = y - old_y, x - old_x   # 何マス分動いたか
        # 左右方向に動く
        if(change_y == 0):  
            distance = x_Distance * change_x
            if(distance > 0):   # 左に動く
                direction = "left"
            if(distance < 0):   # 右に動く
                direction = "right"
                distance = -distance
        # 上下方向に動く
        else:                
            distance = y_Distance * change_y
            if(distance > 0):   # 上に動く
                direction = "forward"
            if(distance < 0):   # 後ろに動く
                direction = "back"
                distance = -distance
        send(f"{direction} {distance}")
        time.sleep(5)
    old_y, old_x = y, x
# ☆☆☆

# 着陸
send("land")
receive()

# ソケットを閉じる
sock.close()



"""
send("forward" "100")
sleep(5)
とかすると100cm動いた後5秒止まるのではなく,前に動いてる時間も5秒の内に含まれるから実質止まるのは3秒ぐらいになる.
"""
