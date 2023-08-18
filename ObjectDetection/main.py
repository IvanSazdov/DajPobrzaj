import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
from supervision.detection.line_counter import LineZone


def main():
    cap = cv2.VideoCapture('media/traffic_short.mp4')
    model = YOLO('models/yolov8x.pt')
    box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=1)
    counter = 0
    b = LineZone


    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        y = frame.shape[0] - 300

        result = model(frame)[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[detections.class_id == 2 ]
        detections = detections[detections.confidence > 0.5]

        labels = [
            f"#1 {model.model.names[class_id]} {confidence:0.2f}"
            for _,_, confidence, class_id, tracker_id
            in detections
        ]
        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        frame = cv2.line(frame, (0, y), (frame.shape[1], y), (0, 0, 255), thickness=2)

        print(detections.tracker_id)
        cv2.imshow("video", frame)
        if cv2.waitKey(20) == 27:
            break

    print(counter)


if __name__ == '__main__':
    main()

# 14
