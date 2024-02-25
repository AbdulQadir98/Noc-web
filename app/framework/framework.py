import os
import numpy as np
import cv2
from ultralytics import YOLO


class NocturneFramework:
    def __init__(self, camera_index=0, app='web'):
        self.camera_index = camera_index
        self.app = app
        self.cap = cv2.VideoCapture(camera_index)
        self.weights = self.get_weights()
        self.models = self.build_models()
        self.running = False

    def __del__(self):
        self.cap.release()

    def build_models(self):
        # model1 = YOLO('yolov8n.pt')
        # model2 = YOLO('yolov5xu.pt')
        # model3 = YOLO('yolov5l6u.pt')

        models = []
        for weight in self.weights:
            path = 'app/models/' + weight
            models.append(YOLO(path))
        return models

    def ensemble(self, frame, results_list):
        all_boxes = []
        # all_confs = []
        # all_class_ids = []

        # Iterate over results from each model
        for results in results_list:
            for r in results:
                boxes = r.boxes.xyxy.cpu().numpy().astype(int)
                # confidences = r.boxes.conf.cpu().numpy().astype(float)
                # class_ids = r.boxes.cls.cpu().numpy().astype(int)

                # Append bounding boxes, confidences, and class IDs to the lists
                all_boxes.append(boxes)
                # all_confs.append(confidences)
                # all_class_ids.append(class_ids)

        # Convert lists to numpy arrays
        all_boxes = np.concatenate(all_boxes)
        # all_confs = np.concatenate(all_confs)
        # all_class_ids = np.concatenate(all_class_ids)

        for box in all_boxes:
            x, y, x2, y2 = box
            w = x2 - x
            h = y2 - y
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # label = f'id: {int(class_id)}, c: {conf:.2f}'
            # cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    def process_frame(self, frame):
        # results = self.model(frame)

        # # Make predictions with each model
        # results1 = model1('/content/ped.jpg')
        # results2 = model2('/content/ped.jpg')
        # results3 = model3('/content/ped.jpg')

        # results = [results1, results2, results3]

        results_list = []
        
        for model in self.models:
            results_list.append(model(frame))

        self.ensemble(frame, results_list)
        return frame

    def start_video(self):
        self.running = True
        while self.running:
            success, frame = self.cap.read()
            if not success:
                break

            frame = self.process_frame(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            if self.app == 'web':
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                return frame

    def stop_video(self):
        self.running = False

    def get_weights(self):
        folder_path = "app/models"
        extension = ".pt"

        # Get the list of models with pt extension
        files = [file for file in os.listdir(
            folder_path) if file.endswith(extension)]

        return files
