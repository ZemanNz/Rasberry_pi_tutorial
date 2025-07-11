import torch
import cv2

# 🧠 Načti model (včetně weights)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/nik/yolov5/runs/train/cubes-exp1/weights/best.pt')

# 🔧 Nastavení (volitelné)
model.conf = 0.45  # minimální confidence (0–1)
model.iou = 0.85  # potlačování překrývajících se boxů
model.classes = None  # nebo např. [0,1] jen některé třídyq

# 📸 Načti obrázek nebo video
cap = cv2.VideoCapture(0)  # nebo 'video.mp4', nebo 'obrazek.jpg'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 📤 Pošli snímek modelu
    results = model(frame)

    # 📊 Výstupy: DataFrame (class, x1, y1, x2, y2, conf, name)
    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        conf_text = f"{label} {conf:.2f}"

        # 🎯 Nakresli box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, conf_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    # 🖼️ Zobraz
    cv2.imshow("YOLOv5 Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
