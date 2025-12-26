import streamlit as st
import os
import json
import shutil
from pathlib import Path


from extract_text import extract_text_from_image
from preprocess_image import preprocess_image
from ai_organizor import extract_fields_as_json
from pdf_to_images import convert_pdf_to_images

# Set up page config
st.set_page_config(
    page_title="OCR Document Processor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    div[data-testid="stExpander"] {
        background-color: #1e2130;
        border: 1px solid #2e3241;
        border-radius: 5px;
    }
    .json-container {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2e3241;
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border: none;
    }
    .success-message {
        color: #4CAF50;
        font-weight: bold;
    }
    .error-message {
        color: #f44336;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def process_single_image(image_path, api_key, temp_dir):
    """Process a single image: preprocess -> OCR -> JSON"""
    try:
        # Preprocess
        preprocessed_path = os.path.join(temp_dir, "preprocessed.jpg")
        preprocess_image(image_path, preprocessed_path)
        
        # OCR
        ocr_text = extract_text_from_image(preprocessed_path)
        
        if not ocr_text.strip():
            return None, "No Text"
        
        # AI JSON extraction
        json_data = extract_fields_as_json(ocr_text, api_key)
        
        if "error" in json_data:
            return None, json_data["error"]
        
        return json_data, None
    except Exception as e:
        return None, str(e)



def save_json_file(json_data, filename, subfolder=None):
    """Save JSON data to file in output folder"""

    # Create output folder if it doesn't exist
    if subfolder:
        output_folder = os.path.join("output", subfolder)
    else:
        output_folder = "output"
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to output folder
    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)
    
    return output_path

# Streamlit App
def main():
    st.title("📄 OCR Document Processor")
    st.markdown("---")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Cerebras API Key", type="password", help="Enter your Cerebras API key")
        st.markdown("---")
        st.markdown("### About")
        st.info("Upload images or PDFs to extract structured data using OCR and AI.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Image or PDF", 
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'pdf'],
        help="Upload an image or PDF document"
    )
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        base_filename = os.path.splitext(uploaded_file.name)[0]
        
        # Check if API key is provided
        if not api_key:
            st.error("⚠️ Please enter your Cerebras API key in the sidebar")
            return
        
        # Create temp directory in same folder
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Process IMAGE
            if file_extension in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif']:
                st.subheader(f"Processing Image: {uploaded_file.name}")
                
                # Save uploaded file
                image_path = os.path.join(temp_dir, uploaded_file.name)
                with open(image_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                with st.spinner("Processing image..."):
                    json_data, error = process_single_image(image_path, api_key, temp_dir)
                
                if error:
                    st.error(f"Erroooor!!!: {error}")
                else:
                    st.success("Processing complete (nice)")
                    
                    # Display JSON
                    st.markdown("### Extracted Data")
                    with st.expander("View JSON", expanded=True):
                        st.json(json_data)
                    
                    # Save button
                    json_filename = f"{base_filename}.json"
                    output_path = save_json_file(json_data, json_filename)
                    
                    st.success(f"✅ JSON saved to: {output_path}")
            
            # Process PDF
            elif file_extension == 'pdf':
                st.subheader(f"Processing PDF: {uploaded_file.name}")
                
                # Save uploaded PDF
                pdf_path = os.path.join(temp_dir, uploaded_file.name)
                with open(pdf_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Convert PDF to images
                pdf_images_folder = os.path.join(temp_dir, "pdf_pages")
                
                with st.spinner("Converting PDF to images..."):
                    try:
                        convert_pdf_to_images(pdf_path, pdf_images_folder)
                        # count images
                        image_files = [f for f in os.listdir(pdf_images_folder) if f.endswith('.jpg')]
                        image_paths = [os.path.join(pdf_images_folder, f) for f in sorted(image_files)]
                        st.success(f"Converted {len(image_paths)} pages (niiiice)")
                    except Exception as e:
                        st.error(f"Error converting PDF (baaaad): {str(e)}")
                        return
                
                # Page selection
                st.markdown("### Select Pages to Process")
                page_numbers = list(range(1, len(image_paths) + 1))
                selected_pages = st.multiselect(
                    "Choose pages",
                    page_numbers,
                    default=page_numbers,
                    help="Select which pages you want to process"
                )
                
                if not selected_pages:
                    st.warning("Select a page a sahbi")
                    return
                
                # Process button
                if st.button("Process Selected Pages"):
                    # Process each selected page
                    for page_num in selected_pages:
                        image_path = image_paths[page_num - 1]
                        
                        st.markdown(f"#### Page {page_num}")
                        
                        with st.spinner(f"Processing page {page_num}..."):
                            json_data, error = process_single_image(image_path, api_key, temp_dir)
                        
                        if error:
                            st.error(f"(oh no) Error on page {page_num}: {error}")
                        else:
                            st.success(f"(yeesss) Page {page_num} complete!")
                            
                            # Display JSON for this page
                            with st.expander(f"View Page {page_num} JSON", expanded=False):
                                st.json(json_data)
                            
                            # Save to folder with PDF name
                            json_filename = f"page_{page_num}.json"
                            output_path = save_json_file(json_data, json_filename, base_filename)
                            
                            st.success(f"Saved to: {output_path}")
                        
                        st.markdown("---")
                
                # Cleanup option
                st.markdown("---")
                cleanup = st.checkbox("🧹 Clean up temporary files", value=True)
                
                if cleanup and st.button("Clean Temp Files"):
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                        st.success("Cleaned Temp Files")
                
                if not cleanup:
                    st.info(f"Temporary files kept in: temp/")
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()