import time
from djitellopy import Tello

# djitellopyを使って他の動作を制御
tello = Tello()

# Telloと接続
tello.connect()
time.sleep(3)

# 離陸コマンドを送信

tello.takeoff()
time.sleep(3)

# 上昇
tello.move_up(20)
time.sleep(3)

# 着陸
tello.land()
time.sleep(5)

# Telloの接続を終了
tello.end()
