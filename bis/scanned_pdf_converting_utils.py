"""
This utility file contains a function which can be called to convert scanned pdf to text
Tesseract-OCR engine needed to be installed!!!
SEE README.md for directions to install Tesseract-OCR engine

Industrial-level implementation with parquet output support.
"""

from pdf2image import convert_from_path
import pytesseract
import os
from pdf_output_utils import save_pdf_extraction_result


def convert_scanned_pdf(pdf_path, ocr_path=None, output_file_path=None, save_parquet=True, output_dir="./data", dpi=400):
    """
    Convert scanned PDF to text using OCR and save in industrial formats.
    
    Args:
        pdf_path (str): Path to the scanned PDF to be converted
        ocr_path (str, optional): Path to the Tesseract OCR executable. If None, uses environment variable TESSERACT_PATH
        output_file_path (str, optional): Path to save the text output
        save_parquet (bool): Whether to save results as parquet (default is True)
        output_dir (str): Directory to save output files (default is "./data")
        dpi (int): DPI for PDF to image conversion (default is 400)
        
    Returns:
        str: The extracted text from the PDF
    """
    # Set the tesseract-OCR path from parameter or environment variable
    if ocr_path:
        pytesseract.pytesseract.tesseract_cmd = ocr_path
    elif os.environ.get('TESSERACT_PATH'):
        pytesseract.pytesseract.tesseract_cmd = os.environ.get('TESSERACT_PATH')
    
    # Split the pdf and create image for each pdf page
    page_images = convert_from_path(pdf_path, dpi=dpi)

    # Extract text from each page
    output_txt = ''
    for page in page_images:
        text = pytesseract.image_to_string(page, lang='eng')
        output_txt += text
    
    # Use the industrial output utility if parquet is requested
    if save_parquet:
        save_text = output_file_path is not None
        result_paths = save_pdf_extraction_result(
            output_txt, 
            pdf_path, 
            output_dir=output_dir,
            save_text=save_text,
            save_parquet=save_parquet
        )
        
        # If output_file_path was provided but we're using the utility,
        # update the path to match what the user expected
        if output_file_path and 'text' in result_paths:
            os.rename(result_paths['text'], output_file_path)
    # Otherwise just use the original text file output
    elif output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(output_txt)
    
    return output_txt

            
if __name__ == '__main__':
    # Path to the scanned PDF to be converted to text
    pdf_path = r'C:\Users\jeff1\Downloads\scanned_pdf.pdf'

    # Path to the OCR engine tesseract.exe location 
    ocr_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Output directory for industrial format outputs
    output_dir = r'C:\Users\jeff1\Documents\pdf_outputs'
    
    # Extract text and save in both text and parquet formats
    extracted_text = convert_scanned_pdf(
        pdf_path=pdf_path,
        ocr_path=ocr_path,
        output_dir=output_dir,
        save_parquet=True
    )
    
    print(f"Extracted {len(extracted_text)} characters from PDF")
