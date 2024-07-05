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

# 画像を二値化し、重心を計算する関数
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

    # ノイズを減らすためにモルフォロジー変換を使用
    kernel = np.ones((5, 5), np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)

    # グレースケールに変換して二値化
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 重心を計算
    moments = cv2.moments(binary)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        return result, binary, (cx, cy)
    return result, binary, (None, None)

# 最小二乗法で直線フィットを行う関数
def least_squares_fit(binary_image):
    y_coords, x_coords = np.where(binary_image == 255)  # 白色のピクセル座標を取得
    print("y_coords", y_coords)
    print("x_coords", x_coords)

    if len(x_coords) > 0:  # 座標が存在するか確認
        # y座標をstepピクセルごとにグループ化してx座標の平均を計算
        grouped_y_coords = []
        grouped_x_coords = []
        
        step = 50
        for y in range(0, max(y_coords) + step, step):
            mask = (y_coords >= y) & (y_coords < y + step)
            if np.any(mask):
                avg_y = np.mean(y_coords[mask])
                avg_x = np.mean(x_coords[mask])
                grouped_y_coords.append(avg_y)
                grouped_x_coords.append(avg_x)
        print("grouped_y_coords", grouped_y_coords)
        print("grouped_x_coords", grouped_x_coords)

        A = np.vstack([grouped_x_coords, np.ones(len(grouped_x_coords))]).T  # 行列を作成
        m, c = np.linalg.lstsq(A, grouped_y_coords, rcond=None)[0]  # 最小二乗法で直線をフィット
        return m, c, grouped_x_coords, grouped_y_coords  # 傾きと切片を返す
    return None, None, [], []  # 座標が存在しない場合

# サンプル画像を読み込む
image_path = "../img/whileLine1.jpg"
image = cv2.imread(image_path)

# 画像が正しく読み込まれたか確認
if image is None:
    print(f"Error: Unable to open image file at {image_path}")
    exit(1)

# 関数を使用して白色部分の抽出と重心の計算を行う
result, binary, (cx, cy) = threshold_centroid(image)

# 重心を描画
if cx is not None and cy is not None:
    cv2.circle(result, (cx, cy), 5, (0, 255, 0), -1)  # 重心に緑の円を描画
    print(f"Centroid coordinates: ({cx}, {cy})")
else:
    print("No centroid found.")

# 最小二乗法で直線フィッティング
m, c, grouped_x_coords, grouped_y_coords = least_squares_fit(binary)

# グループ化された座標を描画
for (x, y) in zip(grouped_x_coords, grouped_y_coords):
    cv2.circle(result, (int(x), int(y)), 5, (0, 0, 255), -1)  # 赤色の点をプロット

# 直線を描画
if m is not None:
    rows, cols = binary.shape
    x1, y1 = 0, int(c)
    x2, y2 = cols, int(m * cols + c)
    cv2.line(result, (x1, y1), (x2, y2), (255, 0, 0), 2)  # 直線を青色で描画
    print(f"Line slope: {m}, intercept: {c}")
else:
    print("No line found.")

# 結果を表示
cv2.imshow('Extracted White Line with Centroid and Fit Line', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
