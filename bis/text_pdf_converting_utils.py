"""
This utility file contains a function which can be called to convert text-pdf to text
We prefer using the pdfplumber library over other options due to its MIT license,
which is known for its permissiveness.

Industrial-level implementation with parquet output support.
"""

import pdfplumber
import os
from pdf_output_utils import save_pdf_extraction_result

def convert_text_from_pdf(pdf_path, output_file_path=None, save_parquet=True, output_dir="./data"):
    """
    Extract text content from a PDF using pdfplumber library.

    Args:
        pdf_path (str): The path to the input PDF file.
        output_file_path (str, optional): The path to the output text file (default is None).
        save_parquet (bool): Whether to save results as parquet (default is True).
        output_dir (str): Directory to save output files (default is "./data").

    Returns:
        str: The extracted text from the PDF.
    """
    output_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Check if text extraction was successful
                output_text += page_text

    # Use the industrial output utility if parquet is requested
    if save_parquet:
        save_text = output_file_path is not None
        result_paths = save_pdf_extraction_result(
            output_text, 
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
        with open(output_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(output_text)

    return output_text

if __name__ == "__main__":
    pdf_file_path = r"E:\5990\pdf\E2438.pdf"
    output_dir = r"E:\5990\output"
    
    # Extract text and save in both text and parquet formats
    extracted_text = convert_text_from_pdf(
        pdf_path=pdf_file_path,
        output_dir=output_dir,
        save_parquet=True
    )
    
    print(f"Extracted {len(extracted_text)} characters from PDF")
