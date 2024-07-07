import socket

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

send("command")
receive()

send("takeoff")
time.sleep(5)

distance = 50
send(f"up {distance}")
time.sleep(5)

send("land")
receive()

# ソケットを閉じる
sock.close()