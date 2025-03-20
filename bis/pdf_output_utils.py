"""
Utility functions for saving PDF extraction results in industrial formats.
"""
import os
import pandas as pd
from datetime import datetime

def save_pdf_extraction_result(text, pdf_path, output_dir="./data", save_text=True, save_parquet=True):
    """
    Save PDF extraction results in multiple formats.
    
    Args:
        text (str): The extracted text from the PDF
        pdf_path (str): The path to the original PDF file
        output_dir (str): Directory to save output files
        save_text (bool): Whether to save as text file
        save_parquet (bool): Whether to save as parquet file
        
    Returns:
        dict: Paths to the saved files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get PDF filename without extension
    pdf_filename = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(pdf_filename)[0]
    
    # Add timestamp to avoid overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_output_name = f"{pdf_name}_{timestamp}"
    
    result_paths = {}
    
    # Save as text file if requested
    if save_text:
        text_path = os.path.join(output_dir, f"{base_output_name}.txt")
        with open(text_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        result_paths['text'] = text_path
    
    # Save as parquet file if requested
    if save_parquet:
        # Create a DataFrame with metadata and content
        df = pd.DataFrame({
            'pdf_name': [pdf_name],
            'original_path': [pdf_path],
            'extraction_time': [datetime.now().isoformat()],
            'content': [text]
        })
        
        parquet_path = os.path.join(output_dir, f"{base_output_name}.parquet")
        df.to_parquet(parquet_path, index=False)
        result_paths['parquet'] = parquet_path
    
    return result_paths
