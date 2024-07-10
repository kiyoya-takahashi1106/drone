import cv2
import numpy as np
import matplotlib.pyplot as plt

# 画像を読み込み
image_path = 'C:\\Users\\daiko\\drone\\img\\redLine50_1.jpg'
image = cv2.imread(image_path)

# BGR画像をHSVに変換
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 赤色の範囲を定義（HSV空間）
lower_red = np.array([0, 100, 100])  # ここを調整して範囲を絞ります
upper_red = np.array([10, 255, 255])  # ここを調整して範囲を絞ります

lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

# 赤色のマスクを作成
mask1 = cv2.inRange(hsv, lower_red, upper_red)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# マスクを適用して赤色部分を抽出
red_only = cv2.bitwise_and(image, image, mask=mask)

# グレースケールに変換
gray = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)

# 重心を計算
M = cv2.moments(gray)
if M["m00"] != 0:
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # 重心を画像上に描画
    cv2.circle(image, (cX, cY), 5, (0, 255, 0), -1)  # 緑色の円で重心を描画
    cv2.putText(image, "centroid", (cX - 25, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 赤以外の部分を白にする
image_with_white_background = np.where(mask[:, :, None] == 0, 255, image)

# 結果を表示
plt.imshow(cv2.cvtColor(image_with_white_background, cv2.COLOR_BGR2RGB))
plt.title('Image with Red Area and Centroid')
plt.axis('off')  # 軸をオフにする
plt.show()
