import numpy as np

def remove_isolated_points(grouped_x_coords, grouped_y_coords, radius):
    filtered_x_coords = []
    filtered_y_coords = []
    for i in range(len(grouped_x_coords)):
        x = grouped_x_coords[i]
        y = grouped_y_coords[i]
        # 周囲の点をチェック
        distances = np.sqrt((grouped_x_coords - x) ** 2 + (grouped_y_coords - y) ** 2)
        # 半径内に他の点があるかチェック
        if np.sum((distances < radius) & (distances > 0)) > 0:
            filtered_x_coords.append(x)
            filtered_y_coords.append(y)
    return np.array(filtered_x_coords), np.array(filtered_y_coords)