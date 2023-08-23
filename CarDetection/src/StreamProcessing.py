import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry import Polygon, Point
from datetime import datetime

class StreamProcessing:
    def __init__(self, name, area, file_path):
        self.name = name
        self.area = area
        self.file_path = file_path

    def Process(self):
        current_minute = datetime.now().minute
        model = YOLO("models/yolov8x.pt")

        polygon = Polygon(self.area)

        cap = cv2.VideoCapture(self.file_path)

        dict = {}
        cars = set()
        frame_counter = 0

        while cap.isOpened():
            success, frame = cap.read()
            frame_counter += 1
            if current_minute != datetime.now().hour:
                current_minute=datetime.now().hour

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

                    # cv2.polylines(annotated_frame, [np.array(self.area, np.int32)], True, (255, 255, 0), 3)
                    #
                    # cv2.putText(annotated_frame,
                    #             str(len(cars)),
                    #             (annotated_frame.shape[1] // 2, annotated_frame.shape[0] // 2),
                    #             cv2.FONT_HERSHEY_SIMPLEX,
                    #             5,
                    #             (255, 0, 0),
                    #             5)
                    # newX = int(annotated_frame.shape[1] * 0.75)
                    # newY = int(annotated_frame.shape[0] * 0.75)
                    # dim = (newX, newY)
                    # annotated_frame = cv2.resize(annotated_frame, dim, interpolation=cv2.INTER_AREA)
                    # cv2.imshow(self.name, annotated_frame)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    break
            else:
                continue
        print(self.name, " : ", len(cars))
