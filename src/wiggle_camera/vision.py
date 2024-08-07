from skimage import measure
import numpy as np
from PIL import Image, ImageDraw
import numpy as np

def calculate_diff_and_find_contours(image, compared_to_image, threshold):
    # Calculate the difference
    diff = image.astype(int) - compared_to_image.astype(int)

    # Find contours for lighter and darker areas
    contours_lighter = measure.find_contours(diff, threshold)
    contours_darker = measure.find_contours(-diff, threshold)

    lighter_pixels = np.sum(diff > threshold)
    darker_pixels = np.sum(diff < -threshold)

    return contours_lighter, contours_darker, lighter_pixels, darker_pixels

def get_contours_by_size(contours, image, small_contour_threshold):
    small_contour_list = []
    large_contour_list = []
    
    for contour in contours:
        # Create a binary image for the contour
        contour_image = np.zeros_like(image)
        contour_image[np.round(contour[:, 0]).astype(int), np.round(contour[:, 1]).astype(int)] = 1

        # Calculate the area of the contour
        area = np.sum(contour_image)
        
        if area < small_contour_threshold:
            small_contour_list.append(contour)
        else:
            large_contour_list.append(contour)
    
    return small_contour_list, large_contour_list

def get_contour_info_and_contours(image, compared_to_image, output_file, threshold=10, small_contour_threshold=40):
    # Calculate difference and find contours
    contours_lighter, contours_darker, lighter_pixels, darker_pixels = calculate_diff_and_find_contours(image, compared_to_image, threshold)

    # Get contours by size
    small_contours_lighter, large_contours_lighter = get_contours_by_size(contours_lighter, image, small_contour_threshold)
    small_contours_darker, large_contours_darker = get_contours_by_size(contours_darker, image, small_contour_threshold)

    # Calculate total areas
    total_area_lighter_small = sum([np.sum(contour) for contour in small_contours_lighter])
    total_area_lighter_large = sum([np.sum(contour) for contour in large_contours_lighter])
    total_area_darker_small = sum([np.sum(contour) for contour in small_contours_darker])
    total_area_darker_large = sum([np.sum(contour) for contour in large_contours_darker])

    # Save the contours image
    save_contours_image(image, small_contours_lighter, large_contours_lighter, small_contours_darker, large_contours_darker, output_file)

    # Create a dictionary to store the results
    return {
        'lighter_count_pixels': lighter_pixels,
        'lighter_small_count': len(small_contours_lighter),
        'lighter_small_total_area': total_area_lighter_small,
        'lighter_large_count': len(large_contours_lighter),
        'lighter_large_total_area': total_area_lighter_large,
        'darker_count_pixels': darker_pixels,
        'darker_small_count': len(small_contours_darker),
        'darker_small_total_area': total_area_darker_small,
        'darker_large_count': len(large_contours_darker),
        'darker_large_total_area': total_area_darker_large
    }

def save_contours_image(image, small_contours_lighter, large_contours_lighter, small_contours_darker, large_contours_darker, output_filename):
    # Convert the grayscale image to RGB
    image_rgb = Image.fromarray(np.uint8(image)).convert('RGB')

    # Create a draw object
    draw = ImageDraw.Draw(image_rgb)

    # Function to draw contours
    def draw_contours(contours, color):
        for contour in contours:
            if isinstance(contour[0], (list, np.ndarray)) and len(contour[0]) == 2:
                contour = [(x[0], x[1]) for x in contour]  # Convert contour points to tuples
                draw.polygon(contour, outline=color)
            else:
                print(f"Unexpected format for contour: {contour}")

    # Draw the contours in different colors
    draw_contours(small_contours_lighter, 'blue')
    draw_contours(large_contours_lighter, 'green')
    draw_contours(small_contours_darker, 'orange')
    draw_contours(large_contours_darker, 'red')

    # Save the image
    image_rgb.save(output_filename)