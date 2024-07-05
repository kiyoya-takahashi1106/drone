# 2値化
import cv2
import numpy as np

# 画像を二値化し
def threshold_centroid(image):
    # BGRからHSVに変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 白色の範囲を定義
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 50, 255], dtype=np.uint8)

    # 白色のマスクを作成
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # マスクを適用して白い部分を抽出
    result = cv2.bitwise_and(image, image, mask=mask)

    # グレースケールに変換して二値化
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    return binary