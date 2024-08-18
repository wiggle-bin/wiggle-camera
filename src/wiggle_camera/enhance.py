from pathlib import Path
import shutil
from PIL import Image
import zipfile

HOME_FOLDER = Path.home()
BASE_FOLDER = HOME_FOLDER / "WiggleBin"
ENHANCED_FOLDER = BASE_FOLDER / "enhanced_temp"
ZIP_FOLDER = BASE_FOLDER / "zips" / "hourly"
VIDEO_FOLDER = BASE_FOLDER / "videos"

import os
from PIL import Image, ImageEnhance, ImageFilter

def enhance_image(image_path, output_path, contrast_factor=2.0, brightness_factor=1.5, sharpness_factor=2.0):
    """
    Enhances the image by adjusting contrast, brightness, and sharpness.
    
    :param image_path: Path to the input image
    :param output_path: Path to save the enhanced image
    :param contrast_factor: Factor by which the contrast will be increased
    :param brightness_factor: Factor by which the brightness will be increased
    :param sharpness_factor: Factor by which the sharpness will be increased
    """
    # Load the image
    image = Image.open(image_path)
    
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
    
    # Save the enhanced image
    image.save(output_path)
    # print(f"Enhanced image saved to: {output_path}")

# Loop over each zip file in the zips folder
for zip_file in ZIP_FOLDER.glob("*.zip"):
    if zip_file.name == "2024-06-09-09.zip":
        continue

    # Create a temporary folder to extract the zip file
    temp_folder = ZIP_FOLDER / "temp"
    temp_folder.mkdir(exist_ok=True)
    enhanced_folder = ZIP_FOLDER / "enhanced_temp"
    enhanced_folder.mkdir(exist_ok=True)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)
    
    # Loop over each image file in the extracted folder
    for image_file in temp_folder.glob("*.jpg"):
        # Generate the output path for the enhanced image
        enhanced_image_path = enhanced_folder / image_file.name
        
        # Enhance the image
        enhance_image(image_file, enhanced_image_path)
    
    # Create a new zip file with the enhanced images
    enhanced_zip_path = ZIP_FOLDER / f"{zip_file.stem}.zip"
    with zipfile.ZipFile(enhanced_zip_path, 'w') as zip_ref:
        for image_file in enhanced_folder.glob("*.jpg"):
            zip_ref.write(image_file, arcname=image_file.name)
    
    # Remove the temporary folder
    shutil.rmtree(temp_folder)
    shutil.rmtree(enhanced_folder)
    
    print(f"Enhanced zip file created: {enhanced_zip_path}")