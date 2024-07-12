# あんまり消したくない

from binarization import binarization
from remove_noise import remove_noise
from remove_isolated_points import remove_isolated_points
from group_coordinates import group_coordinates
from center_leastSquare import center_leastSquare
import cv2
import numpy as np

image_path = r'C:\Users\daiko\drone\img\redLine4.jpg'
Cell_size = 6
Threshold = 0.7
Step = 20
Radius = 40

image = cv2.imread(image_path)
binary_image = binarization(image)
denoised_image = remove_noise(binary_image, Cell_size, Threshold)
y_coords, x_coords = np.where(denoised_image == 255)
grouped_x_coords, grouped_y_coords = group_coordinates(x_coords, y_coords, Step)
filtered_x_coords, filtered_y_coords = remove_isolated_points(grouped_x_coords, grouped_y_coords, Radius)
cx, cy, m = center_leastSquare(filtered_x_coords, filtered_y_coords)
print("(cx, cy, m)", cx, cy, m)