import cv2
import numpy as np
from PIL import Image
import os

def preprocess_image(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale - this is all most OCR engines need
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Subtle sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)

    # save
    cv2.imwrite(output_path, sharpened)
    
    return sharpened


def preprocess_batch(input_folder, output_folder):
    """
    Preprocess all images in a folder.
    """

    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image extensions
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
    
    # Process all images in the input folder
    processed_count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"processed_{filename}")
            
            try:
                preprocess_image(input_path, output_path)
                processed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    print(f"\nTotal images processed: {processed_count}")


# Example usage
if __name__ == "__main__":

    # Single image preprocessing
    input_image = "image.png" 
    output_image = "preprocessed_document.jpg"
    
    # Check if input file exists
    if os.path.exists(input_image):
        preprocessed = preprocess_image(input_image, output_image)
        print("Single image preprocessing completed!")
    else:
        print(f"Input image '{input_image}' not found.")
        print("Please update the input_image variable with your image path.")
    
    # Batch processing
    # preprocess_batch("input_images", "preprocessed_images")