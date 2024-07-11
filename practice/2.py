# hough変換
import cv2
import numpy as np

# 画像を読み込む
image_path = r'C:\Users\daiko\drone\img\redLine4.jpg'
img = cv2.imread(image_path)

# BGRからHSVに変換
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 赤色の範囲を定義（赤色は2つの範囲をカバーするため、2つのマスクを作成）
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

# 赤色のマスクを作成
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# 元の画像を灰色に変換
black_img = np.zeros_like(img)

# 赤色部分を白に変換
result_img = np.where(mask[:, :, np.newaxis] == 255, [255, 255, 255], black_img)

# データ型をuint8に変換
result_img = result_img.astype(np.uint8)

# 結果を表示
cv2.imshow('Red to White', result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()