# Tello自動操縦サンプルコード1

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

# SDKモードを開始
send("command")
receive()

# 離陸
send("takeoff")
time.sleep(8)

# 上昇
send("up 100")
time.sleep(8)

# 下降
send("down 100")
time.sleep(5)

# 着陸
send("land")
receive()

# ソケットを閉じる
sock.close()