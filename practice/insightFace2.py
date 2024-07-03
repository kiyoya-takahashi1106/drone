# insightface2.pyの複数version
# ラグは少しあるもののほぼリアルタイム

import cv2   # 画像処理と表示
import numpy as np
from insightface.app import FaceAnalysis   # 顔検出と特徴量の抽出
import os   # ファイル操作用

# 類似度の算出のための関数（コサイン類似度）
def cos_sim(feat1, feat2):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))

# 検出ボックスと名前を描画するための関数
def draw_on(img, faces, name):
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if face.kps is not None:
            kps = face.kps.astype(int)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color, 2)
        cv2.putText(dimg, name, (box[0]-1, box[1]-4), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 2)

    return dimg

# 閾値の設定
threshold = 0.75

# 顔検出のオブジェクトのインスタンス化
app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))   # GPUを使用する設定, CPUなら-1

# 画像フォルダのパス
img_folder_path = 'C:\\Users\\daiko\\drone\\img'
known_face_names = []
pre_embeddings = []

# フォルダ内のすべての画像を読み込み、特徴量を抽出する
for file_name in os.listdir(img_folder_path):
    if file_name.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(img_folder_path, file_name)
        pre_img = cv2.imread(img_path)
        if pre_img is None:
            print(f"Cannot open or read the image file: {img_path}")
            continue

        pre_face = app.get(pre_img)   # 特徴量抽出
        if len(pre_face) == 0:
            print(f"No face detected in the image: {img_path}")
            continue

        known_face_names.append(file_name)
        pre_embeddings.append(pre_face[0].embedding)

capture = cv2.VideoCapture(0)   # ウェブカメラを起動

# ウィンドウの設定
cv2.namedWindow("Face", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Face", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

recognition_enabled = True

while True:
    ret, frame = capture.read()   # retがFalseならループ終了
    if not ret:
        break

    if recognition_enabled:
        # カメラ画像から顔の検出と特徴量の抽出
        faces = app.get(frame)
        if len(faces) == 0:
            detect = frame
            name = "Unknown"
        else:
            embeddings = faces[0].embedding   # 検出された顔の特徴量を抽出します。

            # 類似度算出と判定
            best_sim = 0
            best_name = "Unknown"
            for i, pre_embedding in enumerate(pre_embeddings):
                sim = cos_sim(pre_embedding, embeddings)
                if sim > best_sim:
                    best_sim = sim
                    if sim >= threshold:
                        best_name = known_face_names[i]
                    else:
                        best_name = "Unknown"

            # 結果の表示
            detect = draw_on(frame, faces, best_name)
    else:
        detect = frame

    cv2.imshow("Face", detect)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        recognition_enabled = not recognition_enabled

capture.release()
cv2.destroyAllWindows()