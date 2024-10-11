import os
from pathlib import Path
from datetime import datetime
from picamera2 import Picamera2
import time
from PIL import Image
import zipfile
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from wiggle_camera.write import write_to_csv, write_rows_to_csv, remove_columns_from_csv
from wiggle_camera.timelapse import create_timelapse, create_timelapse
from wiggle_camera.vision import calculate_diff
from wiggle_camera.object_detection import perform_inference

HOME_FOLDER = Path.home()
BASE_FOLDER = HOME_FOLDER / "WiggleBin"
IMG_FOLDER = BASE_FOLDER / "pictures"
ZIP_FOLDER = BASE_FOLDER / "zips"
VIDEO_FOLDER = BASE_FOLDER / "videos"

def create_directory():
    os.makedirs(IMG_FOLDER, exist_ok=True)

create_directory()

def picture(folder=IMG_FOLDER):
    previousImage = Image.open(folder / "latest.jpg").convert('L')
    filePath = folder / "latest.jpg"
    picture_gray(filePath, previousImage)

def picture_color(filePath):
    picam2 = Picamera2()
    WIDTH = 1024
    HEIGHT = 768
    config = picam2.create_preview_configuration(
        {"size": (WIDTH, HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)
    picam2.capture_file(str(filePath))
    picam2.close()

def enhance_image(image, contrast_factor=2.0, brightness_factor=1.5, sharpness_factor=2.0):    
    # Adjust contrast
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(contrast_factor)
    
    # Adjust brightness
    brightness_enhancer = ImageEnhance.Brightness(image)
    image = brightness_enhancer.enhance(brightness_factor)
    
    # Adjust sharpness
    sharpness_enhancer = ImageEnhance.Sharpness(image)
    image = sharpness_enhancer.enhance(sharpness_factor)
    
    # Convert to grayscale
    image = image.convert("L")
    
    # Apply a sharpen filter
    image = image.filter(ImageFilter.SHARPEN)
    
    return image

def picture_gray(filePath, previousImage):
    grey = picture_yuv()
    mean_gray_value = grey.mean()
    image = Image.fromarray(grey)
    image = enhance_image(image)
    image.save(filePath)
    (zipName, fileName) = add_to_zip(filePath)
    store_vision_data(mean_gray_value, filePath, previousImage, zipName, fileName)

def store_vision_data(mean_gray_value, filePath, previousImage, zipName, fileName):
    now = datetime.now()

    # Predictions
    inference_data = perform_inference(filePath)
    predictions = inference_data.get('predictions', [])

    for item in predictions:
        item.update({
            "time": now.isoformat(),
            "filename": fileName,
            "zip": zipName
        })
        item.pop("image_path", None)
        item.pop("prediction_type", None)

    write_rows_to_csv(predictions, 'image-predictions', [
        "time",
        "filename",
        "x",
        "y",
        "width",
        "height",
        "class",
        "confidence",
        "zip"
    ])

    # Image data
    sensor_data = {
        "time": now.isoformat(),
        "mean_gray": mean_gray_value,
        "detection_confidence_min": min([item['confidence'] for item in predictions], default=0),
        "detection_confidence_max": max([item['confidence'] for item in predictions], default=0),
        "detection_confidence_avg": np.mean([item['confidence'] for item in predictions]) if predictions else 0,
        "detection_count": len(predictions),
        "detection_class_worm_count": len([item for item in predictions if item['class'] == 'worm']),
        "detection_class_fly_count": len([item for item in predictions if item['class'] == 'fly']),
        "detection_class_fly_larva_count": len([item for item in predictions if item['class'] == 'fly-larva'])
    }

    if (previousImage):
        image = Image.open(filePath).convert('L')
        image_comparison_data = calculate_diff(np.array(image), np.array(previousImage))
        sensor_data.update(image_comparison_data)

    write_to_csv(sensor_data, 'image-data', [
        "time", 
        "mean_gray",
        "count_pixels_lighter",
        "count_pixels_darker",
        "detection_confidence_min",
        "detection_confidence_max",
        "detection_confidence_avg",
        "detection_count",
        "detection_class_worm_count",
        "detection_class_fly_count",
        "detection_class_fly_larva_count",
    ])

def add_to_zip(filePath):
    now = datetime.now()
    fileName = now.strftime("%Y-%m-%d-%H-%M") + ".jpg"

    zipName = add_file_to_zip("%Y-%m-%d-%H", "hourly", filePath, fileName)

    # add to daily zip if it is the 10th minute of the hour
    if now.minute % 10 == 0:
        add_file_to_zip("%Y-%m-%d", "daily", filePath, fileName)
    # add to weekly zip if it is the first minute of the hour    
    if now.minute == 1:
        add_file_to_zip("%Y-%W", "weekly", filePath, fileName)
    # create new hourly timelapse if it is the last minute of the hour 
    if now.minute == 59:
        create_timelapse("hourly", now.strftime("%Y-%m-%d-%H"))
     # create new daily timelapse if it is the last minute of the day
    if now.hour == 23 and now.minute == 59:
        create_timelapse("daily", now.strftime("%Y-%m-%d"))
    # create new weekly timelapse if it is the last minute of the week
    if now.weekday() == 6 and now.hour == 23 and now.minute == 59:
        create_timelapse("weekly", now.strftime("%Y-%W"))

    return (zipName, fileName)

def add_file_to_zip(time, subFolder, filePath, fileName):
    now = datetime.now()
    zipName = now.strftime(time)
    zipPath = ZIP_FOLDER / subFolder / (zipName + ".zip")
    os.makedirs(zipPath.parent, exist_ok=True)
    with zipfile.ZipFile(zipPath, "a") as zipf:
        zipf.write(filePath, arcname=fileName)
    return zipName

def picture_yuv():
    WIDTH = 1024
    HEIGHT = 768
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        {"format": "YUV420", "size": (WIDTH, HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()
    yuv = picam2.capture_array()
    grey = yuv[:HEIGHT, :WIDTH]
    picam2.close()
    return grey


def recording():
    seconds = 60
    try:
        while True:
            picture()
            time.sleep(seconds)
    except KeyboardInterrupt:
        print("Stopped by User")


def start_recording():
    os.system("systemctl --user start wiggle_record.service")


def stop_recording():
    os.system("systemctl --user stop wiggle_record.service")
