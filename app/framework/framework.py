import os
import cv2
from ultralytics import YOLO


class NocturneFramework:
    def __init__(self, camera_index=0, app='web', model_path='yolov5s.pt'):
        self.camera_index = camera_index
        self.app = app
        self.cap = cv2.VideoCapture(camera_index)
        # self.model = YOLO(model_path)
        self.running = False

    def __del__(self):
        self.cap.release()

    def process_frame(self, frame):
        results = self.model(frame)
        for detection in results:
            x, y, w, h, class_id, confidence = detection
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'{self.model.names[int(class_id)]} {confidence:.2f}', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame

    def start_video(self):
        self.running = True
        while self.running:
            success, frame = self.cap.read()
            if not success:
                break

            # frame = self.process_frame(frame)

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
