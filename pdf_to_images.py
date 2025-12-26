import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path, output_folder):

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    try:
        # Convert PDF pages to a list of PIL Image objects, dpi=300 std high qlty
        
        print("Converting pages... beee patient")
        pages = convert_from_path(pdf_path, dpi=300)

        for i, page in enumerate(pages):
            # Define finename
            image_name = f"page_{i + 1}.jpg"
            image_path = os.path.join(output_folder, image_name)
            
            # Save the image
            page.save(image_path, "JPEG")
            print(f"Saved: {image_name}")

        print("\nConversion complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    input_pdf = "rapport.pdf" 
    target_folder = "pdf_pages_output"

    convert_pdf_to_images(input_pdf, target_folder)