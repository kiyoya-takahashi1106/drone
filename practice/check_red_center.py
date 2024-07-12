import cv2
import numpy as np
import matplotlib.pyplot as plt


def binarization(image_path):
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


def remove_noise(binary_image, cell_size, threshold):
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


def remove_isolated_points(grouped_x_coords, grouped_y_coords, radius):
    filtered_x_coords = []
    filtered_y_coords = []
    for i in range(len(grouped_x_coords)):
        x = grouped_x_coords[i]
        y = grouped_y_coords[i]
        # 周囲の点をチェック
        distances = np.sqrt((grouped_x_coords - x) ** 2 + (grouped_y_coords - y) ** 2)
        # 半径内に他の点があるかチェック
        if np.sum((distances < radius) & (distances > 0)) > 0:
            filtered_x_coords.append(x)
            filtered_y_coords.append(y)
    return np.array(filtered_x_coords), np.array(filtered_y_coords)


def center_least_squares(filtered_x_coords, filtered_y_coords):
    if len(filtered_x_coords) > 0:
        # 重心を計算
        cx = np.mean(filtered_x_coords)
        cy = np.mean(filtered_y_coords)

        # 最小二乗法
        A = np.vstack([filtered_x_coords, np.ones(len(filtered_x_coords))]).T
        m, _ = np.linalg.lstsq(A, filtered_y_coords, rcond=None)[0]
        m = -m

        # デバッグ用のプリント文
        print("(m):", m)
        print("(cx):", cx)
        print("(cy):", cy)

        return cx, cy, m
    return None, None, None


def plot_results(original_image, binary_image, denoised_image, cx, cy, m, filtered_x_coords, filtered_y_coords):
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
            ax.plot(filtered_x_coords, filtered_y_coords, 'bo')  # グループ化された座標をプロット
            ax.plot(cx, cy, 'ro')  # 重心を赤い点でプロット

    plt.show()


# テスト用の画像パスを設定
image_path = r'C:\Users\daiko\drone\img\redLine5.jpg'
# image_path = r'C:\Users\daiko\drone\img\redLine_test\redLine150_1.jpg'

# 二値化を行う
original_image, binary_image = binarization(image_path)

# ノイズ除去を行う
denoised_image = remove_noise(binary_image.copy(), 6, 0.7)   # 数値の入力はcell_size, 閾値

# 白いピクセルの座標を抽出
y_coords, x_coords = np.where(denoised_image == 255)

# 残った点をグループ化
grouped_x_coords, grouped_y_coords = group_coordinates(x_coords, y_coords, 20)   # 数値の入力はstep数

# 孤立した点を削除
filtered_x_coords, filtered_y_coords = remove_isolated_points(grouped_x_coords, grouped_y_coords, 40)   # 数値の入力は半径

# 最小二乗法と重心を計算
cx, cy, m = center_least_squares(filtered_x_coords, filtered_y_coords)

# 結果をプロット
plot_results(original_image, binary_image, denoised_image, cx, cy, m, filtered_x_coords, filtered_y_coords)