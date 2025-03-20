#!/usr/bin/env python
"""
Main script to run the entire BIS ETL pipeline.
This script orchestrates the execution of all data extraction, transformation, and loading processes.
"""

import os
import argparse
import logging
from datetime import datetime
from bis.aav_scraping import main as run_aav_scraping
from bis.ev_scraping import main as run_ev_scraping

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"etl_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the environment for the ETL pipeline."""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    logger.info(f"Data directory set up at: {data_dir}")
    
    # Set Tesseract path from environment variable if available
    tesseract_path = os.environ.get('TESSERACT_PATH')
    if tesseract_path:
        logger.info(f"Using Tesseract OCR from: {tesseract_path}")
    else:
        logger.warning("TESSERACT_PATH environment variable not set. OCR functionality may be limited.")
    
    return data_dir

def run_web_scraping():
    """Run all web scraping modules."""
    logger.info("Starting web scraping processes...")
    
    try:
        logger.info("Running anti-boycott violations scraping...")
        run_aav_scraping()
        logger.info("Anti-boycott violations scraping completed successfully.")
    except Exception as e:
        logger.error(f"Error in anti-boycott violations scraping: {str(e)}")
    
    try:
        logger.info("Running export violations scraping...")
        run_ev_scraping()
        logger.info("Export violations scraping completed successfully.")
    except Exception as e:
        logger.error(f"Error in export violations scraping: {str(e)}")
    
    logger.info("Web scraping processes completed.")

def main():
    """Main function to run the ETL pipeline."""
    parser = argparse.ArgumentParser(description='Run the BIS ETL pipeline')
    parser.add_argument('--skip-scraping', action='store_true', help='Skip web scraping steps')
    args = parser.parse_args()
    
    logger.info("Starting BIS ETL pipeline...")
    
    # Setup environment
    data_dir = setup_environment()
    
    # Run web scraping if not skipped
    if not args.skip_scraping:
        run_web_scraping()
    else:
        logger.info("Web scraping skipped as requested.")
    
    logger.info("BIS ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
