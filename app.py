from flask import Flask, request, jsonify, render_template, send_file
import torch
import argparse
import sys
from pathlib import Path
from ultralytics import YOLO
import os

app = Flask(__name__)

# Model paths
MODEL_PATHS = {
    'acne': 'models/acne_best_250epochs.pt',
    'redness': 'models/redness_model.pt',
    'eyebag': 'models/eyebag_new_best.pt',
    'wrinkle': 'models/wrinkle_best.pt'
}

# Load models
models = {}
for name, path in MODEL_PATHS.items():
    try:
        models[name] = YOLO(path)
    except Exception as e:
        print(f"Error loading model {name}: {str(e)}")

def run_prediction(model_name, image_path):
    if model_name not in models:
        return {"error": f"Model {model_name} not found"}
    
    try:
        results = models[model_name](image_path)
        predictions = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                pred = {
                    'x1': float(box.xyxy[0][0]),
                    'y1': float(box.xyxy[0][1]),
                    'x2': float(box.xyxy[0][2]),
                    'y2': float(box.xyxy[0][3]),
                    'confidence': float(box.conf[0]),
                    'class': int(box.cls[0]),
                    'class_name': result.names[int(box.cls[0])]
                }
                predictions.append(pred)
        
        return {
            "model": model_name,
            "predictions": predictions
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html', models=list(MODEL_PATHS.keys()))

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    model_name = request.form.get('model', 'acne')
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save the uploaded file temporarily
    temp_path = Path("temp_upload.jpg")
    file.save(temp_path)
    
    # Run prediction
    result = run_prediction(model_name, str(temp_path))
    
    # Clean up
    temp_path.unlink()
    
    return jsonify(result)

def cli():
    parser = argparse.ArgumentParser(description='Run YOLOv8 model predictions')
    parser.add_argument('--model', type=str, required=True, choices=list(MODEL_PATHS.keys()),
                      help='Model to use for prediction')
    parser.add_argument('--image', type=str, required=True,
                      help='Path to the image file')
    
    args = parser.parse_args()
    
    result = run_prediction(args.model, args.image)
    print(result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cli()
    else:
        app.run(debug=True, port=5000)
