import numpy as np

def calculate_diff(image, compared_to_image, threshold=10):
    # Calculate the difference
    diff = image.astype(int) - compared_to_image.astype(int)

    lighter_pixels = np.sum(diff > threshold)
    darker_pixels = np.sum(diff < -threshold)

    return {
        'count_pixels_lighter': lighter_pixels,
        'count_pixels_darker': darker_pixels,
    }
