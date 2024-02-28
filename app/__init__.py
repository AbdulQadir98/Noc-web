from app.framework.framework import NocturneFramework
from app.models import *
from app.views import *
from flask import Flask, render_template, request, Response, redirect, url_for
import os

framework = NocturneFramework()

# Create a Flask application instance
app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html', models=framework.get_weights())


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


@app.route('/video_feed')
def video_feed():
    return Response(framework.start_video(), mimetype='multipart/x-mixed-replace; boundary=frame')
