import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry import Polygon, Point


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)


cv2.namedWindow('Traffic')
cv2.setMouseCallback("Traffic", RGB)

model = YOLO('models/yolov8n.pt')

video_path = "media/premin_blace.mp4"
cap = cv2.VideoCapture(video_path)


area_premin = [(499, 341), (241, 539), (1446, 557), (1240, 325)]
polygon = Polygon(area_premin)
dict = {}

print(dict.get(1))
cars = set()
frame_counter = 0

while cap.isOpened():
    success, frame = cap.read()
    frame_counter += 1

    if frame_counter % 3 == 0:
        if success:
            results = model.track(frame, persist=True)

            annotated_frame = results[0].plot()

            for box in results[0].boxes:
                if box.id is None:
                    continue
                x1 = box.xyxy[0][0]
                x2 = box.xyxy[0][2]
                y1 = box.xyxy[0][1]
                y2 = box.xyxy[0][3]

                cx = int(x1 + x2) // 2
                cy = int(y1 + y2) // 2
                point = [Point(cx, cy), int(box.id)]

                annotated_frame = cv2.circle(annotated_frame, (cx, cy), 3, thickness=1, color=(0, 255, 0))

                if polygon.contains(point[0]):
                    if dict.get(point[1]) is None:
                        dict[point[1]] = 0
                    dict[point[1]] = dict[point[1]] + 1
                    cars.add(point[1])

            cv2.polylines(frame, [np.array(area_premin, np.int32)], True, (255, 255, 0), 3)

            cv2.putText(annotated_frame,
                        str(len(cars)),
                        (annotated_frame.shape[1] // 2, annotated_frame.shape[0] // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        5,
                        (255, 0, 0),
                        5)
            newX = int(annotated_frame.shape[1] * 0.75)
            newY = int(annotated_frame.shape[0] * 0.75)
            dim = (newX, newY)
            annotated_frame = cv2.resize(annotated_frame, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow("Traffic", frame)

            if cv2.waitKey(0) & 0xFF == ord("q"):
                break
        else:
            break
    else:
        continue

print("Number of cars:", len(cars))
print("Frame counter:", frame_counter)
print(dict)

cap.release()
cv2.destroyAllWindows()
