import numpy as np

m = -2
tan_theta = 1 / m
radians_error = np.arctan(tan_theta)   # arctan関数を使用して角度θをラジアンで求める
angle_error = np.degrees(radians_error) 
print(angle_error)