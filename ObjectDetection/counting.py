import cv2
from pathlib import Path
import torch


class VideoLineCounter:
    def __init__(self, model_path):
        # Load YOLO model
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

        # Variables to store last detected object midpoints
        self.last_midpoints = {}

    def process_frame(self, frame, line_position):
        # Run inference on the current frame
        results = self.model(frame)
        detections = results.pred[0]

        # Filter out detections with a confidence less than 0.5 and class_id 2
        detections = [x for x in detections if x[2] > 0.5 and int(x[5]) == 2]

        counter = 0
        for det in detections:
            x1, y1, x2, y2 = map(int, det[:4])
            mid_y = (y1 + y2) // 2

            obj_id = (x1, y1, x2, y2)
            if obj_id in self.last_midpoints:
                # Check if object crossed the line
                if self.last_midpoints[obj_id] < line_position and mid_y >= line_position:
                    counter += 1
                elif self.last_midpoints[obj_id] > line_position and mid_y <= line_position:
                    counter += 1

            # Update last midpoint
            self.last_midpoints[obj_id] = mid_y

        # Draw the line on the frame
        cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (0, 0, 255), 2)

        return frame, counter

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        total_count = 0
        line_position = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 300

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame, count = self.process_frame(frame, line_position)
            total_count += count

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == 27:  # ESC key
                break

        cap.release()
        cv2.destroyAllWindows()
        return total_count


if __name__ == '__main__':
    counter = VideoLineCounter(model_path='path_to_your_model.pt')
    total_objects_crossed = counter.process_video('media/traffic_short.mp4')
    print(f"Total objects crossed the line: {total_objects_crossed}")
