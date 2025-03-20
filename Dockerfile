FROM python:3.9-slim

# Install system dependencies for Tesseract OCR and pdf2image
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create data directory
RUN mkdir -p data

# Set environment variable for Tesseract
ENV TESSERACT_PATH=/usr/bin/tesseract

# Command to run when container starts
# This is a placeholder - you can override with specific scripts
CMD ["python", "-m", "bis.aav_scraping"]
