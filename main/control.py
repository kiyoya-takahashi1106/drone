# 制御
import math
import numpy as np

def control(prevDistance, img_width, img_height, cx, cy, m):   # 一つ前の行動の進んだ距離, 重心x座標, 重心y座標, 画像の幅, 画像の高さ, 傾き
    # 今の角度から垂直にする角度
    tan_theta = 1 / m
    radians_error = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
    angle_error = np.degrees(radians_error)   # ラジアンを度に変換
    angle_error = int(angle_error)

    # y方向のずれ
    y_error = prevDistance - prevDistance * math.cos(radians_error)
    y_error = int(y_error)

    # x方向のずれ
    # こっち側から重心までのy(img_height - cy)を入れたら, real/droの画面 比率が分かる.
    fx = 0.001265 * np.exp(0.018237 * (img_height - cy)) + 0.367068

    # 重心cxと画面中心のずれ(d)
    cx_middle_error = img_width//2 - cx

    # drone画面のx方向のずれを入れたら, y軸を基準とする実際のx方向のずれが分かる.
    x_error = -cx_middle_error * fx
    x_error = int(x_error)

    return angle_error, y_error, x_error