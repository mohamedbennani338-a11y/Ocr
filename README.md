# OCR Document Processor

A web-based OCR application that extracts structured data from images and PDFs using AI.

## Requirements

Install the following libraries:

```bash
pip install streamlit
pip install pytesseract
pip install Pillow
pip install opencv-python
pip install pdf2image
pip install cerebras-cloud-sdk
```

## Additional Setup

- Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Install [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) (for PDF conversion)

## Running the Project

```bash
streamlit run main.py
```

## Usage

1. Enter your Cerebras API key in the sidebar
2. Upload an image or PDF file
3. For PDFs, select which pages to process
4. View and save the extracted JSON data

## Output

- JSON files are saved in the `output/` folder
- For images: `output/filename.json`
- For PDFs: `output/pdf_name/page_1.json`, `page_2.json`, etc.
