# 制御
import numpy as np

def contorl(direction, cx, cy, width, height, m):   # 重心x座標, 重心y座標, 画像の幅, 画像の高さ, 傾き
        # 今の角度から垂直にする角度
        tan_theta = m
        theta_radians = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
        angle_error = np.degrees(theta_radians)   # ラジアンを度に変換


    return angle_error