import os
from pathlib import Path
from datetime import datetime
from picamera2 import Picamera2
import time
from PIL import Image
import zipfile

from wiggle_camera.timelapse import create_timelapse, create_timelapse

HOME_FOLDER = Path.home()
BASE_FOLDER = HOME_FOLDER / "WiggleBin"
IMG_FOLDER = BASE_FOLDER / "pictures"
ZIP_FOLDER = BASE_FOLDER / "zips"
VIDEO_FOLDER = BASE_FOLDER / "videos"

def create_directory():
    os.makedirs(IMG_FOLDER, exist_ok=True)

create_directory()

def picture(folder=IMG_FOLDER):
    filePath = folder / "latest.jpg"
    picture_gray(filePath)

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


def picture_gray(filePath):
    grey = picture_yuv()
    image = Image.fromarray(grey)
    image.save(filePath)
    add_to_zip(filePath)

def add_to_zip(filePath):
    now = datetime.now()

    add_file_to_zip("%Y-%m-%d-%H", "hourly", filePath)
    # add to daily zip if it is the 10th minute of the hour
    if now.minute % 10 == 0:
        add_file_to_zip("%Y-%m-%d", "daily", filePath)
    # add to weekly zip if it is the first minute of the hour    
    if now.minute == 1:
        add_file_to_zip("%Y-%W", "weekly", filePath)
    # create new hourly timelapse if it is the last minute of the hour 
    if now.minute == 59:
        create_timelapse("hourly", now.strftime("%Y-%m-%d-%H"), "hourly")
     # create new daily timelapse if it is the last minute of the day
    if now.hour == 23 and now.minute == 59:
        create_timelapse("daily", now.strftime("%Y-%m-%d"), "daily")

def add_file_to_zip(time, subFolder, filePath):
    now = datetime.now()
    zipName = now.strftime(time)
    zipPath = ZIP_FOLDER / subFolder / (zipName + ".zip")
    os.makedirs(zipPath.parent, exist_ok=True)
    with zipfile.ZipFile(zipPath, "a") as zipf:
        zipf.write(filePath, arcname=now.strftime("%Y-%m-%d-%H-%M") + ".jpg")

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
