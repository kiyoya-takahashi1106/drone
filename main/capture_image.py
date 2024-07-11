import cv2

def capture_image():
    cap = cv2.VideoCapture('udp://0.0.0.0:11111')
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None

    ret, frame = cap.read()
    if ret:
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)
        print(f"Image captured and saved to {image_path}")
        cap.release()
        return image_path
    else:
        print("Error: Could not read frame.")
        cap.release()
        return None