from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load your trained model
MODEL_PATH = 'Model.h5'
model = load_model(MODEL_PATH)

# Class labels used during training
class_labels = [
    'Colon Adenocarcinoma',
    'Colon Benign Tissue',
    'Lung Adenocarcinoma',
    'Lung Benign Tissue',
    'Lung Squamous Cell Carcinoma'
]

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save uploaded image
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Preprocess image for model
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

        # Prediction
        preds = model.predict(img_array)
        pred_class = class_labels[np.argmax(preds)]

        confidence = round(np.max(preds) * 100, 2)

        return render_template('result.html', 
                               image_file=file.filename,
                               prediction=pred_class,
                               confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)
