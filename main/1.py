# あんまり消したくない

from threshold import threshold
from center_leastSquare import center_leastSquare
import cv2

image_path = r'C:\Users\daiko\drone\img\redLine4.jpg'
image = cv2.imread(image_path)
binary = threshold(image)
cx, cy, m = center_leastSquare(binary)
print(cx, cy, m)