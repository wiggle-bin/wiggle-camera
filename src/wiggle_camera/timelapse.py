from pathlib import Path
import subprocess
import zipfile
import shutil

HOME_FOLDER = Path.home()
BASE_FOLDER = HOME_FOLDER / "WiggleBin"
IMG_FOLDER = BASE_FOLDER / "pictures"
VIDEO_FOLDER = BASE_FOLDER / "videos"
ZIP_FOLDER = BASE_FOLDER / "zips"

def create_timelapse(subFolder, date, outputName):
    zip_file = ZIP_FOLDER / subFolder / f"{date}.zip"
    video_file = VIDEO_FOLDER / f"{outputName}.mp4"

    temp_folder = BASE_FOLDER / "temp"
    temp_folder.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)

    subprocess.run(
        [
            "ffmpeg",
            "-y",  # Add the -y flag to overwrite the output file if it already exists
            "-r",
            "10",
            "-pattern_type",
            "glob",
            "-i",
            str(temp_folder / "*.jpg"),
            "-c:v",
            "libx264",
            "-vf",
            "fps=25",
            "-pix_fmt",
            "yuv420p",
            str(video_file),
        ]
    )

    if temp_folder.exists():
        shutil.rmtree(temp_folder)

if __name__ == "__main__":
    create_timelapse("daily", "2024-06-02", "daily")