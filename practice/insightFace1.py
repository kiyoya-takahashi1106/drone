# webカメラに映った顔の顔認識

import cv2   # 画像処理と表示
import numpy as np
from insightface.app import FaceAnalysis   # 顔検出と特徴量の抽出

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
            #print(landmark.shape)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color, 2)
        cv2.putText(dimg, name, (box[0]-1, box[1]-4), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 2)

    return dimg

# 画像のパス指定と閾値の設定
pre_img_path = 'C:\\Users\\daiko\\drone\\img\\kiyoya2.jpg'
threshold = 0.75

# 顔検出のオブジェクトのインスタンス化
app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))   # GPUを使用する設定, CPUなら-1

# 登録画像の読み込みと特徴量の抽出
pre_img = cv2.imread(pre_img_path)
if pre_img is None:
    raise ValueError(f"Cannot open or read the image file: {pre_img_path}")

pre_face = app.get(pre_img)   # 特徴量抽出
if len(pre_face) == 0:
    raise ValueError("No face detected in the preloaded image.")
pre_embedding = [pre_face[0].embedding]

known_face_name = ["Unknown", "kiyoya"]

capture = cv2.VideoCapture(0)   # ウェブカメラを起動

# ウィンドウの設定
cv2.namedWindow("Face", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Face", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = capture.read()   # retがFalseならループ終了
    if not ret:
        break

    # カメラ画像から顔の検出と特徴量の抽出
    faces = app.get(frame)
    if len(faces) == 0:
        detect = frame
        name = "Unknown"
    else:
        embeddings = faces[0].embedding   # 検出された顔の特徴量を抽出します。

        # 類似度算出
        sim = cos_sim(pre_embedding[0], embeddings)
        # 閾値を超えた際に、登録された人物であると判定
        if sim >= threshold:
            name = known_face_name[1]
        else:
            name = known_face_name[0]

        # 結果の表示
        detect = draw_on(frame, faces, name)

    cv2.imshow("Face", detect)

    # qを押すと終了
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

capture.release()
cv2.destroyAllWindows()
