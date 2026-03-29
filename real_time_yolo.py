# real_time_yolo.py
# 实时摄像头 + YOLO 人体检测 + 画框 + 显示人数
from ultralytics import YOLO
import cv2

# 加载模型
model = YOLO("yolov8n.pt")

# 打开摄像头
cap = cv2.VideoCapture(0)

# Mac 摄像头需要设置分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✅ 实时检测已启动")
print("按 q 键退出窗口")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 推理
    results = model(frame, verbose=False)

    # 统计人数
    person_count = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # 只检测人
                person_count += 1

                # 画框
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 在画面上写字：显示人数
    cv2.putText(
        frame,
        f"People: {person_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 0, 255),
        3
    )

    # 显示画面
    cv2.imshow("DeskGuard AI 实时检测", frame)

    # 按 q 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()