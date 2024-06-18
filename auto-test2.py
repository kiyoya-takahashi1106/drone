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
y_Distance = 30
x_Distance = 50
root = [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2], [1, 2], [1, 3], [1, 2]]   # (y, x)

for i, x, y in enumerate(root):   # i:idxnum
    if(i == 0):
        pass
    else:
        change_y, change_x = y - old_y, x - old_x   # 何マス分動いたか
        if(change_y == 0):   # x方向に動く
            direction = "left"
            distance = x_Distance * change_x
        else:                # y方向に動く
            directionhoge = "forward"
            distance = y_Distance * change_y
        send(f"{direction} {distance}")
        time.sleep(5)
    old_y, old_x = y, x
# ☆☆☆

# 着陸
send("land")
receive()

# ソケットを閉じる
sock.close()
