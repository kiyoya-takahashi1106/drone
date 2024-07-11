# 重心計算 & 最小二乗法
import cv2
import numpy as np

def center_leastSquare(denoise_image):
    # 重心計算
    moments = cv2.moments(denoise_image)   # モーメントを計算
    if moments["m00"] != 0:   # 重心が存在するか確認
        cx = int(moments["m10"] / moments["m00"])   # 重心のX座標を計算
        cy = int(moments["m01"] / moments["m00"])   # 重心のY座標を計算
    else:
        cx, cy = None, None   # 重心が存在しない場合
    

    # 最小二乗法
    # 白色のピクセル座標を取得(y,x_coordsは配列)
    y_coords, x_coords = np.where(denoise_image == 255)  # 白色のピクセル座標を取得

    if len(x_coords) > 0:  # 座標が存在するか確認
        # y座標をstepピクセルごとにグループ化してx座標の平均を計算
        grouped_y_coords = []
        grouped_x_coords = []
        
        step = 20
        for y in range(0, max(y_coords) + step, step):
            mask = (y_coords >= y) & (y_coords < y + step)
            if np.any(mask):
                avg_y = np.mean(y_coords[mask])
                avg_x = np.mean(x_coords[mask])
                grouped_y_coords.append(avg_y)
                grouped_x_coords.append(avg_x)
        # print("grouped_y_coords", grouped_y_coords)
        # print("grouped_x_coords", grouped_x_coords)

        A = np.vstack([grouped_x_coords, np.ones(len(grouped_x_coords))]).T   # 行列を作成
        m, _ = np.linalg.lstsq(A, grouped_y_coords, rcond=None)[0]   # 最小二乗法で直線をフィット(mx + _)
        m = -m
        return cx, cy, m
    return cx, cy, None   # 座標が存在しない場合