import os
from pathlib import Path
from roboflow import Roboflow
import json

HOME_FOLDER = Path.home()
BASE_FOLDER = HOME_FOLDER / "WiggleBin"
SETTINGS_FILE = BASE_FOLDER / "settings.json"
IMG_FOLDER = BASE_FOLDER / "pictures"
LATEST_IMAGE = IMG_FOLDER / "latest.jpg"

with open(SETTINGS_FILE, 'r') as file:
    config = json.load(file)

roboflow_config = config.get('roboflow')

API_KEY = roboflow_config['api_key']
WORKSPACE = roboflow_config['workspace']
PROJECT = roboflow_config['project']
VERSION_NUMBER = roboflow_config['version']
URL = roboflow_config['url']
CONFIDENCE = roboflow_config.get('confidence', 10)
OVERLAP = roboflow_config.get('overlap', 30)

def perform_inference(image_file = LATEST_IMAGE, confidence=CONFIDENCE, overlap=OVERLAP):
    """
    Perform inference on an image file using a Roboflow model.

    Parameters:
    - image_file (str): Path to the image file.
    - confidence (int): Confidence threshold for predictions.
    - overlap (int): Overlap threshold for predictions.

    Returns:
    - dict: Prediction results in JSON format.
    """
    # Convert image_file to string if it is a Path object
    if isinstance(image_file, Path):
        image_file = str(image_file)

    # Instantiate the Roboflow object and authenticate with your credentials
    rf = Roboflow(api_key=API_KEY)
    
    # Load/connect to your project
    project = rf.workspace(WORKSPACE).project(PROJECT)
    
    # Load/connect to your trained model
    model = project.version(VERSION_NUMBER, local=URL).model
    
    # Perform inference on an image file
    prediction = model.predict(image_file, confidence=confidence, overlap=overlap)
    
    # Save and plot the prediction
    result_path = os.path.join(IMG_FOLDER, "detection.jpg")
    prediction.save(result_path)
    
    # Return the prediction results
    return prediction.json()

if __name__ == "__main__":
    results = perform_inference()
    print(results)