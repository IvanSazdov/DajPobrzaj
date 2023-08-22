import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry.polygon import Polygon, Point

# def RGB(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         colorsBGR = [x, y]
#         print(colorsBGR)
#
#
# cv2.namedWindow('Traffic')
# cv2.setMouseCallback("Traffic", RGB)

model = YOLO('models/yolov8x.pt')

video_path = "media/traffic_short.mp4"
cap = cv2.VideoCapture(video_path)

area_premin = [(581, 298), (345, 448), (1618, 456), (1581, 303)]
area_traffic = [(168, 384), (91, 486), (729, 547), (706, 416)]

polygon = Polygon(area_traffic)
cars = set()
frame_counter = 0
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    frame_counter += 1

    if frame_counter % 3 == 0:
        if success:
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)

            # Visualize the results on the frame
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
                # point = Point(cx,cy)
                annotated_frame = cv2.circle(annotated_frame, (cx, cy), 3, thickness=1, color=(0, 255, 0))

                if polygon.contains(point[0]):
                    cars.add(point[1])

            cv2.polylines(annotated_frame, [np.array(area_traffic, np.int32)], True, (255, 255, 0), 3)

            # Display the annotated frame
            cv2.putText(annotated_frame,
                        str(len(cars)),
                        (annotated_frame.shape[1] // 2, annotated_frame.shape[0] // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        5,
                        (255, 0, 0),
                        5)
            cv2.imshow("Traffic", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break
    else:
        continue

# Release the video capture object and close the display window
print(len(cars))
cap.release()
cv2.destroyAllWindows()
