from flask import Flask, request, jsonify, render_template, send_file
import torch
import argparse
import sys
from pathlib import Path
from ultralytics import YOLO
import os
import base64
from PIL import Image
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor

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

def process_single_model(model_name, image_path):
    try:
        results = models[model_name](image_path)
        result = results[0]
        
        # Convert the result to PIL Image
        result_image = result.plot()
        result_image = Image.fromarray(result_image)
        
        # Convert to base64 for sending to frontend
        buffered = io.BytesIO()
        result_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Get predictions
        predictions = []
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
            "predictions": predictions,
            "result_image": f"data:image/jpeg;base64,{img_str}"
        }
    except Exception as e:
        return {
            "model": model_name,
            "error": str(e)
        }

async def run_all_predictions(image_path):
    # Create a thread pool for running model predictions
    with ThreadPoolExecutor() as executor:
        # Create tasks for each model
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_single_model, model_name, image_path)
            for model_name in models.keys()
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results

@app.route('/')
def home():
    return render_template('index.html', models=list(MODEL_PATHS.keys()))

@app.route('/predict', methods=['POST'])
async def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save the uploaded file temporarily
    temp_path = Path("temp_upload.jpg")
    file.save(temp_path)
    
    try:
        # Run predictions for all models
        results = await run_all_predictions(str(temp_path))
        
        # Clean up
        temp_path.unlink()
        
        return jsonify({
            "results": results,
            "total_models": len(results),
            "successful_predictions": sum(1 for r in results if "error" not in r)
        })
    except Exception as e:
        # Clean up in case of error
        if temp_path.exists():
            temp_path.unlink()
        return jsonify({"error": str(e)}), 500

def cli():
    parser = argparse.ArgumentParser(description='Run YOLOv8 model predictions')
    parser.add_argument('--image', type=str, required=True,
                      help='Path to the image file')
    
    args = parser.parse_args()
    
    # Run predictions for all models
    results = asyncio.run(run_all_predictions(args.image))
    print(results)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cli()
    else:
        app.run(debug=True, port=5000)
