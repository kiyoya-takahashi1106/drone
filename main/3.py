# 消したらあかん
import numpy as np

pc_y_error_lst = [4.5, 6.5, 7.5, 8, 8.5, 8.8, 9, 9.2]
pc_x_error_lst = [2.6, 1.8, 1.4, 1.1, 0.9, 0.8, 0.7, 0.6]

for pc_y_error, pc_x_error in zip(pc_y_error_lst, pc_x_error_lst):
    cy = pc_y_error * 34 / 45
    # こっち側から重心までのy(img_height - cy)を入れたら, real/droの画面 比率が分かる.
    fx = (40 * (1 + np.exp(0.85 * (cy - 5.4)))) / 3.07

    # 重心cxと画面中心のずれ(d)
    cx_middle_error = pc_x_error * 960 / 1280

    # drone画面のx方向のずれを入れたら, 実際のx方向のずれが分かる.
    x_error = cx_middle_error * fx
    print(x_error)
