from ultralytics import YOLO
import cv2
import supervision as sv

box_annotator = sv.BoxAnnotator(thickness=1,text_thickness=1,text_scale=1)
model = YOLO('models/yolov8x.pt')
img = cv2.imread('media/premin.png')
results = model(img)[0]
detections = sv.Detections.from_ultralytics(results)
img = box_annotator.annotate(scene=img,detections=detections)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()


