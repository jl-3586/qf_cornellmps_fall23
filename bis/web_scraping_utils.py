import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://efoia.bis.doc.gov/"

def create_column_selector(column_idx):
    """""
    Create the CSS selector for selecting all values of a specified column index excluding the title and header rows
    
    Args:
        column_num (int): column number/ index for the column to extract from HTML
        
    Returns:
        String: the CSS selector to be passed into soup.select()
    """""
    # :nth-child selects the n-th child of an HTML element. The (n+3) syntax specifies all children after the first two.
    return f'table tr:nth-child(n+3) td:nth-child({column_idx})'


def perform_web_scraping(hompage_url):
    """
    Utilizes BeautifulSoup to perform web scraping based on HTML of the given url
    Extracts case id's, case links, case names and order dates from the HTML and saves to data frame

    Args:
        homepage_url (String): url of the HTML to be scraped

    Returns:
        pandas DataFrame: contains 4 columns storing the scraped results
    """
    
    response = requests.get(hompage_url)
    if response.status_code != 200: raise RuntimeError(f'Error fetching page: status code {response.status_code}')
    
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    id_col_idx = 1
    name_col_idx = 2
    date_col_idx = 3

    case_id_col = soup.select(create_column_selector(id_col_idx))
    case_name_col = soup.select(create_column_selector(name_col_idx))
    order_date_col = soup.select(create_column_selector(date_col_idx))

    case_ids = [case_id.text.strip() for case_id in case_id_col]
    case_links = [urljoin(BASE_URL, case_id.find('a')['href']) for case_id in case_id_col]
    case_names = [case_id.text.strip() for case_id in case_name_col]
    order_dates = [case_id.text.strip() for case_id in order_date_col]

    # Create a pandas DataFrame
    data = {
        'case_id': case_ids,
        'case_link': case_links,
        'case_name': case_names,
        'order_date': order_dates
    }

    return pd.DataFrame(data)