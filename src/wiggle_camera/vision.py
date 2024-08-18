import numpy as np

def calculate_diff(image, compared_to_image, threshold=10):
    # Calculate the difference
    diff = image.astype(int) - compared_to_image.astype(int)

    lighter_pixels = np.sum(diff > threshold)
    darker_pixels = np.sum(diff < -threshold)

    return {
        'lighter_count_pixels': lighter_pixels,
        'darker_count_pixels': darker_pixels,
    }
