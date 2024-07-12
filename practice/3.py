# remove_isolated_pointsを実装していない時のcheck_red_center.py

import cv2
import numpy as np
import matplotlib.pyplot as plt


def threshold(image_path):
    # 画像を読み込む
    image = cv2.imread(image_path)

    # BGRからHSVに変換
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 赤色の範囲を定義（赤色は2つの範囲をカバーするため、2つのマスクを作成）
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # 赤色のマスクを作成
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # マスクを適用して赤い部分を抽出
    result = cv2.bitwise_and(image, image, mask=mask)

    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

    return image, binary_image


def remove_noise(binary_image, cell_size=6, threshold=0.7):
    height, width = binary_image.shape[:2]
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cell = binary_image[y:y+cell_size, x:x+cell_size]
            red_pixels = np.sum(cell == 255)
            total_pixels = cell.size
            red_ratio = red_pixels / total_pixels
            
            if red_ratio < threshold:
                binary_image[y:y+cell_size, x:x+cell_size] = 0

    return binary_image


def center_leastSquare(binary_image):
    moments = cv2.moments(binary_image)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = None, None

    y_coords, x_coords = np.where(binary_image == 255)
    if len(x_coords) > 0:
        grouped_y_coords = []
        grouped_x_coords = []

        step = 20
        for y in range(0, max(y_coords) + step, step):
            mask = (y_coords >= y) & (y_coords < y + step)
            if np.any(mask):
                avg_y = np.mean(y_coords[mask])
                avg_x = np.mean(x_coords[mask])
                grouped_y_coords.append(avg_y)
                grouped_x_coords.append(avg_x)

        A = np.vstack([grouped_x_coords, np.ones(len(grouped_x_coords))]).T
        m, _ = np.linalg.lstsq(A, grouped_y_coords, rcond=None)[0]
        m = -m
        # デバッグ用のプリント文
        print("(m):", m)
        return cx, cy, m, grouped_x_coords, grouped_y_coords
    return cx, cy, None, [], []


def plot_results(original_image, binary_image, denoised_image, cx, cy, m, grouped_x_coords, grouped_y_coords):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)

    # 元画像を表示
    axes[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')
    axes[0].axis('off')  # 軸を表示しない

    # 二値化画像を表示
    axes[1].imshow(binary_image, cmap='gray')
    axes[1].set_title('Binary Image')
    axes[1].axis('off')  # 軸を表示しない

    # ノイズ除去後の画像を表示
    axes[2].imshow(denoised_image, cmap='gray')
    axes[2].set_title('Denoised Image')
    axes[2].axis('off')  # 軸を表示しない

    if cx is not None and cy is not None:
        for ax in axes:
            ax.plot(cx, cy, 'ro')
            # グループ化された座標をプロット
            ax.plot(grouped_x_coords, grouped_y_coords, 'bo')

    plt.show()
    
    
# テスト用の画像パスを設定
image_path = r'C:\Users\daiko\drone\img\redLine5.jpg'
# image_path = r'C:\Users\daiko\drone\img\redLine_test\redLine25_2.jpg'

# 二値化を行う
original_image, binary_image = threshold(image_path)

# ノイズ除去を行う
denoised_image = remove_noise(binary_image.copy())

# 重心と最小二乗法を適用
cx, cy, m, grouped_x_coords, grouped_y_coords = center_leastSquare(denoised_image)

print(grouped_y_coords)
print(grouped_x_coords)

# 結果をプロット
plot_results(original_image, binary_image, denoised_image, cx, cy, m, grouped_x_coords, grouped_y_coords)