# 制御
import math
import numpy as np

def contorl(prevDistance, cx, cy, width, height, m):   # 一つ前の行動の進んだ距離, 重心x座標, 重心y座標, 画像の幅, 画像の高さ, 傾き
    # 今の角度から垂直にする角度
    tan_theta = m
    theta_radians = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
    angle_error = np.degrees(theta_radians)   # ラジアンを度に変換
    
    # y方向のずれ
    if(angle_error < 0):
        abs_angle_error = -angle_error
    else:
        abs_angle_error = angle_error
    y_error = prevDistance - prevDistance * math.sin(angle_error)

    return angle_error, y_error