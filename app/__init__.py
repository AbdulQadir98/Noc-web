import cv2
from app.framework.framework import NocturneFramework
from app.models import *
from app.views import *
from flask import Flask, render_template, request, Response, redirect, url_for
import os

framework = NocturneFramework()

# Create a Flask application instance
app = Flask(__name__)


@app.route('/hello')
def hello():
    return framework.say_hello("Vili")


@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html', models=framework.get_models())


@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'modelFile' in request.files:
        model_file = request.files['modelFile']
        if model_file.filename != '':
            models_folder = os.path.join(app.root_path, 'models')
            model_file.save(os.path.join(models_folder, model_file.filename))
            return redirect(url_for('home'))

    # Handle the case where no file is selected
    return redirect(url_for('home'))


# capturing frames from the camera and yielding them as continuous stream of JPEG images.
def camera_feed():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
