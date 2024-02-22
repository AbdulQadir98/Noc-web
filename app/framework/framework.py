import os
import cv2
from ultralytics import YOLO


class NocturneFramework:
    def __init__(self, camera_index=0, app='web', model_path='app/models/best.pt'):
        self.camera_index = camera_index
        self.app = app
        self.cap = cv2.VideoCapture(camera_index)
        self.model = YOLO(model_path)
        self.running = False

    def __del__(self):
        self.cap.release()

    def process_frame(self, frame):
        results = self.model(frame)
        for detection in results:
            boxes = detection.boxes.xyxy.cpu().numpy().astype(int)
            for (x, y, x2, y2) in boxes:
                w = x2-x
                h = y2-y
                # object_region frame is [x:x+w, y:y+h]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
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

    def get_models(self):
        folder_path = "app/models"
        extension = ".pt"

        # Get the list of models with pt extension
        files = [file for file in os.listdir(
            folder_path) if file.endswith(extension)]

        return files
