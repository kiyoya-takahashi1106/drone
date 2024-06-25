# 複数人の顔認識

import numpy as np
import os   # ファイルやディレクトリ操作用
import cv2
from insightface.app import FaceAnalysis
from glob import glob   # パターンマッチングに基づいてファイルパスを取得するため
from tqdm import tqdm   # プログレスバー表示ライブラリ
from collections import defaultdict   # 存在しないキーに対してデフォルト値を提供
from PIL import Image
from IPython.display import display, Image

# 平均を算出するための関数
def get_averages(names, scores):
    d = defaultdict(list)
    for n, s in zip(names, scores):   # namesとscoresはlst
        d[n].append(s)
    averages = {}
    for n, s in d.items():
        averages[n] = np.mean(s)
    return averages

"""
#認証を行うための関数
def judge_sim(known_embeddings, known_names, unknown_embeddings, threshold):
    pred_names = []
    for emb in unknown_embeddings:
        scores = np.dot(emb, known_embeddings.T)
        scores = np.clip(scores, 0., None)

        averages = get_averages(known_names, scores)
        pred = sorted(averages, key=lambda x: averages[x], reverse=True)[0]
        print(averages)
        score = averages[pred]

        if score > threshold:
            pred_names.append(pred)
        else:
            pred_names.append(None)
    return pred_names
"""

# バウンディングボックスと名前を描画するための関数
def draw_on(img, faces, name):
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if (face.kps is not None):
            kps = face.kps.astype(int)
            #print(landmark.shape)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if (l == 0 or l == 3):
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color, 2)
        cv2.putText(dimg, name[i], (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)
    return dimg

# 名前と特徴量を格納するためのリストの初期化
known_names = []
known_embeddings = []
unknown_embeddings = []

# フォルダの名前を取得
players = os.listdir('C:\\Users\\daiko\\drone\\img\\peoples_face')

# 認証させる画像の登録
img_path = '認証させたい写真のパス'
img = cv2.imread(img_path)

# 登録写真の顔検出を行うための準備
app_pre = FaceAnalysis()
app_pre.prepare(ctx_id=0, det_size=(640, 640))


# 認証写真の顔検出を行うための準備
app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))

# 登録写真の特徴量の計算
for player in tqdm(players):
    player_embeddings, player_names = [], []

    img_paths = glob(f'data/{player}/*')
    
    for img_path in img_paths:
        img = cv2.imread(img_path)
        if img is None: continue

        faces = app_pre.get(np.array(img))
        if len(faces) == 0 : continue
        player_embeddings.append(faces[0].embedding)
        player_names.append(player)

        if len(known_embeddings) == 10: break
    
    player_embeddings = np.stack(player_embeddings, axis=0)
    known_embeddings.append(player_embeddings)
    known_names += player_names
known_embeddings = np.concatenate(known_embeddings, axis=0)

# 顔認証の実施
faces = app.get(np.array(img))

for i in range(len(faces)):
    unknown_embeddings.append(faces[i].embedding)

pred_names = judge_sim(known_embeddings, known_names, unknown_embeddings, 90)

detect = draw_on(img, faces, pred_names)

_, buf = cv2.imencode(".jpg", detect)
display(Image(data=buf.tobytes()))