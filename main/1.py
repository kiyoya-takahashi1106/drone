# まだ消したらあかん
import cv2
import numpy as np

# 重心を計算する関数
def find_centroid(binary_image):
    moments = cv2.moments(binary_image)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        return cx, cy
    return None, None

# サンプル画像を読み込む
image_path = "../img/whileLine1.jpg"
image = cv2.imread(image_path)

# 画像が正しく読み込まれたか確認
if image is None:
    print(f"Error: Unable to open image file at {image_path}")
    exit(1)

# BGRからHSVに変換
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 白色の範囲を定義
lower_white = np.array([0, 0, 200], dtype=np.uint8)
upper_white = np.array([180, 50, 255], dtype=np.uint8)

# 白色のマスクを作成
mask = cv2.inRange(hsv, lower_white, upper_white)

# マスクを適用して白い部分を抽出
result = cv2.bitwise_and(image, image, mask=mask)

# マスクを二値化画像として重心を計算
cx, cy = find_centroid(mask)

# 重心を描画
if cx is not None and cy is not None:
    cv2.circle(result, (cx, cy), 5, (0, 255, 0), -1)  # 重心に緑の円を描画
    print(f"Centroid coordinates: ({cx}, {cy})")
else:
    print("No centroid found.")

# 結果を表示
cv2.imshow('Extracted White Line with Centroid', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
