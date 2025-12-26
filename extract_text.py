import pytesseract
from PIL import Image
import cv2
import os



pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path, lang='eng'):
    """
    Extract text from an image with pytesseract
    """

    try:
        # Open the image
        img = Image.open(image_path)
        
        # custom_config = r'--oem 3 --psm 6'
        # OEM 3 = Default OCR Engine Mode
        # PSM 6 = Assume a single uniform block of text
        
        text = pytesseract.image_to_string(img, lang=lang)
        
        print(f"Text extracted from: {image_path}")
        print("-" * 50)
        
        return text
    
    except Exception as e:
        print(f"Error extracting text from {image_path}: {str(e)}")
        return ""


def extract_text_with_confidence(image_path, lang='eng'):
    """
    Extract text along with confidence scores for each word.
    return Dictionary: text, confidence information
    """
    try:
        img = Image.open(image_path)
        
        # Get data including confidence scores
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        
        # Filter out empty text and low confidence results
        filtered_text = []
        total_confidence = 0
        word_count = 0
        
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])
            
            if text and conf > 0:  # Only include words with confidence > 0
                filtered_text.append(text)
                total_confidence += conf
                word_count += 1
        
        # Calculate average confidence
        avg_confidence = total_confidence / word_count if word_count > 0 else 0
        
        full_text = ' '.join(filtered_text)
        
        result = {
            'text': full_text,
            'average_confidence': round(avg_confidence, 2),
            'word_count': word_count
        }
        
        print(f"Extracted {word_count} words with {avg_confidence:.2f}% average confidence")
        
        return result
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'text': '', 'average_confidence': 0, 'word_count': 0}


def save_extracted_text(text, output_path):
    """
    Save extracted text to a file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text saved to: {output_path}")
    except Exception as e:
        print(f"Error saving text: {str(e)}")


def batch_extract_text(input_folder, output_folder, lang='eng'):
    """
    Extract text from all images in a folder
    """
    os.makedirs(output_folder, exist_ok=True)
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.txt'
            output_path = os.path.join(output_folder, output_filename)
            
            print(f"\nProcessing: {filename}")
            text = extract_text_from_image(input_path, lang)
            
            if text.strip():
                save_extracted_text(text, output_path)
            else:
                print(f"No text found in {filename}")


# Example usage
if __name__ == "__main__":
    # Single image extraction
    input_image = "image.png"  # Use the preprocessed image
    
    if os.path.exists(input_image):
        # Method 1: Simple extraction
        print("\n=== Simple Text Extraction ===")
        extracted_text = extract_text_from_image(input_image)
        print(extracted_text)
        
        # Method 2: Extraction with confidence scores
        print("\n=== Extraction with Confidence ===")
        result = extract_text_with_confidence(input_image)
        print(f"Text: {result['text'][:200]}...")  # Show first 200 chars
        print(f"Average Confidence: {result['average_confidence']}%")
        print(f"Word Count: {result['word_count']}")
        
        # Save to file
        save_extracted_text(extracted_text, "extracted_text.txt")
        
    else:
        print(f"Image '{input_image}' not found.")
        print("Please update the input_image variable with your image path.")
    
    # Batch processing example (uncomment to use)
    # batch_extract_text("preprocessed_images", "extracted_texts")