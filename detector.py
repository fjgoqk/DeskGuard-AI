from ultralytics import YOLO
import cv2
import atexit

model = YOLO("yolov8n.pt")
cap = None

def init_camera():
    global cap
    if cap is None:
        for i in [0, 1, 2]:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                break

def release_camera():
    global cap
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        cap = None

atexit.register(release_camera)

def detect_people():
    init_camera()
    try:
        ret, frame = cap.read()
        if not ret:
            return 0
        results = model(frame, verbose=False)
        count = 0
        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:
                    count += 1
        return count
    except:
        return 0

def is_anyone_looking():
    return detect_people() >= 2