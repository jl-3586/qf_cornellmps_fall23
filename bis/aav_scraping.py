"""
Scrape the BIS alleged anti-boycott violations directory.
Save results as parquet file for industrial-level data storage.
"""
from web_scraping_utils import perform_web_scraping, BASE_URL
import os

def main():
    aav_url = 'https://efoia.bis.doc.gov/index.php/electronic-foia/index-of-documents/7-electronic-foia/226-alleged-antiboycott-violations'

    violation_name = 'alleged-antiboycott-violations'
    df_webpage = perform_web_scraping(aav_url)
    
    # Create output directory if it doesn't exist
    output_dir = "./data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as parquet file
    output_path = f"{output_dir}/{violation_name}.parquet"
    df_webpage.to_parquet(output_path, index=False)
    print(f"Data saved to {output_path}")
    
if __name__ == '__main__':
    main()
