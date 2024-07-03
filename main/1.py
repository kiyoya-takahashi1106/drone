import cv2

def main():
    # カメラをキャプチャ
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("カメラが開けません")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームを取得できませんでした")
            break

        # ここでフレーム処理を行う（例えば、顔認識など）

        cv2.imshow('Camera Frame', frame)

        # 'q'キーを押したら終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

cv2.destroyAllWindows()
