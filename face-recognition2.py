# 複数人の顔認識
# ×

import numpy as np
import os   # ファイルやディレクトリ操作用
import cv2
from insightface.app import FaceAnalysis
from glob import glob   # パターンマッチングに基づいてファイルパスを取得するため
from tqdm import tqdm   # プログレスバー表示ライブラリ
from collections import defaultdict   # 存在しないキーに対してデフォルト値を提供

# 平均を算出するための関数
def get_averages(names, scores):
    d = defaultdict(list)   # キーが存在しない場合にデフォルトで空のリストを提供する辞書を作成。
    for n, s in zip(names, scores):   # namesとscoresは配列
        d[n].append(s)
    averages = {}   # 平均値を格納するための辞書
    for n, s in d.items():   # key値とvalue
        averages[n] = np.mean(s)
    return averages

# 認証を行うための関数
def judge_sim(known_embeddings, known_names, unknown_embeddings, threshold):
            # 既知の顔の特徴量, 既知の名前, 未知の顔の特徴量, 既知
    pred_names = []
    for emb in unknown_embeddings:
        scores = np.dot(emb, known_embeddings.T)
        scores = np.clip(scores, 0., None)   # スコア0以上の値にクリップ
        averages = get_averages(known_names, scores)   # 各名前のスコアの平均値
        pred = sorted(averages, key=lambda x: averages[x], reverse=True)[0]   # 平均スコアが最も高い名前を取得
        score = averages[pred]   # 最も高いスコアを取得
        if score > threshold:   # スコアが閾値を超えているか
            pred_names.append(pred)
        else:
            pred_names.append("Unknown")
    return pred_names

# バウンディングボックスと名前を描画するための関数
def draw_on(img, faces, name):   # 画像, 顔検出結果, 名前lst
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)   # 顔のバウンディングボックスを整数型に変換。
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)   # バウンディングボックスを描画
        if face.kps is not None:
            kps = face.kps.astype(int)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color, 2)
        cv2.putText(dimg, name[i], (box[0]-1, box[1]-4), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    return dimg

# 名前と特徴量を格納するためのリストの初期化
known_names = []   # 既知の名前を格納するリスト
known_embeddings = []   # 既知の顔特徴量を格納するリストを初期化

# フォルダの名前を取得
players = os.listdir('C:\\Users\\daiko\\drone\\img\\peoples_face')

# 登録写真の顔検出を行うための準備
app_pre = FaceAnalysis()
app_pre.prepare(ctx_id=0, det_size=(640, 640))   # CPUを使用

# Webカメラの顔検出を行うための準備
app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))   # CPUを使用

# 登録写真の特徴量の計算
for player in tqdm(players):
    player_names, player_embeddings = [], []
    img_paths = glob(f'C:\\Users\\daiko\\drone\\img\\peoples_face\\{player}\\*')
    for img_path in img_paths:
        img = cv2.imread(img_path)   # 画像を読み込み
        if img is None:   # 画像が読み込めない場合
            continue
        faces = app_pre.get(np.array(img))   # 画像から顔を検出
        if len(faces) == 0:   # 検出できなかったら
            continue
        player_embeddings.append(faces[0].embedding)   # 検出された顔の特徴量をlstに追加
        player_names.append(player)
        if len(known_embeddings) == 10:  
            break
    if player_embeddings:   # 特徴lstが空でなければ
        player_embeddings = np.stack(player_embeddings, axis=0)   # 特徴リストをNumpy配列に変換
        known_embeddings.append(player_embeddings)   # 特徴リストを既知の特徴量リストに追加
        known_names += player_names   # 名前リストを既知の名前リストに追加
if known_embeddings:
    known_embeddings = np.concatenate(known_embeddings, axis=0)   # 特徴量リストを結合
    known_embeddings = np.array(known_embeddings)  # リストからNumPy配列に変換
else:
    known_embeddings = np.array([])  # 空の配列で初期化

# ウェブカメラの映像に対して顔認識を実施
capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:   # フレームが読み込めなかったら
        break
    faces = app.get(np.array(frame))   # フレームから顔を検出し、特徴量を抽出
    unknown_embeddings = []   # 未知の顔特徴量を格納するリスト
    for i in range(len(faces)):   # 検出された顔の分ループ
        unknown_embeddings.append(faces[i].embedding)

    # 未知の顔の特徴量を既知の顔の特徴量と比較し、最も類似度の高い名前を判定
    if known_embeddings.size > 0:  # known_embeddingsが空でないか確認
        pred_names = judge_sim(np.array(known_embeddings), known_names, np.array(unknown_embeddings), 0.5)
    else:
        pred_names = ["Unknown"] * len(faces)  # 全てUnknownとして処理

    # 検出結果を描画
    detect = draw_on(frame, faces, pred_names)
    cv2.imshow("Face Recognition", detect)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()