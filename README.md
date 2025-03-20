# Cornell MPS Capstone Project - Fall 2023

Home directory for the Cornell MPS project for Fall 2023. This project contains a BIS (Bureau of Industry and Security) ETL (Extract, Transform, Load) pipeline.

![2025-03-20_11-10-53](https://github.com/user-attachments/assets/57fc6571-9f3f-40f0-a47c-c97c23313bbd)

## Prerequisites

- Docker and Docker Compose
- For local development: Python 3.9+ and dependencies in requirements.txt
- Tesseract OCR (automatically installed in Docker container)

## Quick Start with Docker

1. Clone the repository
2. Navigate to the project directory
3. Build and run the containers:

```bash
docker-compose up --build
```

This will start the following services:
- `etl-pipeline`: Runs the complete ETL pipeline (recommended for most users)
- `bis-scraper`: Scrapes alleged anti-boycott violations
- `bis-export-violations`: Scrapes export violations
- `pdf-processor`: Example service for PDF processing (requires configuration)

To run just the complete ETL pipeline:

```bash
docker-compose up etl-pipeline
```

## Docker Services

### Running specific services

To run a specific service:

```bash
docker-compose up bis-scraper
```

### Customizing services

Edit the `docker-compose.yml` file to customize services or add new ones.

## Data Output

All data is saved in the `./data` directory, which is mounted as a volume in the Docker containers. This allows data to persist between container runs.

Output formats:
- Parquet files (.parquet): Efficient columnar storage format
- Text files (.txt): Plain text output (optional)

## Development

For local development without Docker:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
   - Windows: Use the installer from https://github.com/UB-Mannheim/tesseract/wiki
   - Mac: `brew install tesseract`
   - Linux: `apt-get install tesseract-ocr`

3. Run the scripts:
```bash
# Run individual scrapers
python -m bis.aav_scraping
python -m bis.ev_scraping

# Or run the complete ETL pipeline
python run_etl_pipeline.py
```

## ETL Pipeline Script

The project includes a comprehensive ETL pipeline script (`run_etl_pipeline.py`) that orchestrates the execution of all data extraction, transformation, and loading processes:

- Sets up the environment (creates directories, configures logging)
- Runs all web scraping modules
- Handles errors gracefully with detailed logging
- Provides command-line options for customization

Command-line options:
```bash
python run_etl_pipeline.py --skip-scraping  # Skip web scraping steps
```

All logs are saved to a timestamped log file for audit and debugging purposes.

## PDF Processing

The project includes utilities for processing both text-based and scanned PDFs:

- `text_pdf_converting_utils.py`: For text-based PDFs
- `scanned_pdf_converting_utils.py`: For scanned PDFs (requires Tesseract OCR)

Example usage:

```python
from bis.text_pdf_converting_utils import convert_text_from_pdf

text = convert_text_from_pdf(
    pdf_path="path/to/pdf",
    output_dir="./data",
    save_parquet=True
)
```
