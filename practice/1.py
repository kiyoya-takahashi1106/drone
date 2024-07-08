import socket
import cv2
import numpy as np

# TelloのIPアドレスとポート
tello_address = ('192.168.10.1', 8889)

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Telloと通信開始
sock.bind(('', 9000))

# Telloにコマンドを送信する関数
def send_command(command):
    sock.sendto(command.encode(), tello_address)

# Telloにコマンドを送信してステータスを受信する関数
def receive_status():
    response, _ = sock.recvfrom(1024)
    return response.decode('utf-8')

# Telloに接続する
send_command('command')
receive_status()

# ストリームを開始する
send_command('streamon')
receive_status()

# フレームを受信して保存する
while True:
    # フレームを受信
    try:
        data, server = sock.recvfrom(1518)
        frame = np.frombuffer(data, dtype=np.uint8)
        frame = np.reshape(frame, (720, 960, 3))

        # 画像を保存する例
        cv2.imwrite('picture.png', frame)

    except Exception as e:
        print(e)
        break

# Telloとの通信を終了する
send_command('streamoff')
receive_status()
receive_status()

# ソケットを閉じる
sock.close()