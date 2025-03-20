Development area for BIS ETL pipeline.

# HOW TO install and use Pytesseract OCR engine
1. Install tesseract OCR
   
   For Windows users: using Windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki
   
   For Mac users: You can install Tesseract using either MacPorts or Homebrew. Check out https://tesseract-ocr.github.io/tessdoc/Installation.html.
   MacPorts: https://ports.macports.org/port/tesseract/

2. Note the tesseract path from the installation.  The installation path for tesseract will be used as the parameter.

3. Install Python package pytesseract using "pip install pytesseract"

4. Set the tesseract path in the script before calling image_to_string:

   pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe' 
   
   Change the path to the location of your tesseract.exe 

