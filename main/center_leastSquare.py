# 重心計算 & 最小二乗法
import numpy as np

def center_leastSquare(filtered_x_coords, filtered_y_coords):
    if len(filtered_x_coords) > 0:
        # 重心を計算
        cx = np.mean(filtered_x_coords)
        cy = np.mean(filtered_y_coords)

        # 最小二乗法
        A = np.vstack([filtered_x_coords, np.ones(len(filtered_x_coords))]).T
        m, _ = np.linalg.lstsq(A, filtered_y_coords, rcond=None)[0]
        m = -m

        return cx, cy, m
    return None, None, None