import numpy as np

def group_coordinates(x_coords, y_coords, step):
    grouped_y_coords = []
    grouped_x_coords = []

    for y in range(0, max(y_coords) + step, step):
        mask = (y_coords >= y) & (y_coords < y + step)
        if np.any(mask):
            avg_y = np.mean(y_coords[mask])
            avg_x = np.mean(x_coords[mask])
            grouped_y_coords.append(avg_y)
            grouped_x_coords.append(avg_x)
    
    return np.array(grouped_x_coords), np.array(grouped_y_coords)