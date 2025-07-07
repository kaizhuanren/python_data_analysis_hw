import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os
from config import CONFERENCE_MAP, START_YEAR, RAW_DATA_PATH, DATA_DIR

def get_papers_for_conference_year(conf_name, conf_short_name, year):
    """
    Modified version with better error handling and URL construction
    """
    current_year = datetime.now().year
    if year > current_year:
        print(f"Skipping {conf_name} {year} - year is in the future")
        return []
    
    if conf_short_name.lower() == 'nips':
        if year >= 2019:
            path_year = f"neurips{year}"
        else:
            path_year = f"nips{year}"
        url = f"https://dblp.org/db/conf/nips/{path_year}.html"
    else:
        url = f"https://dblp.org/db/conf/{conf_short_name}/{conf_short_name}{year}.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Retrying: {conf_name} {year} (URL: {url})")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Retry failed for {conf_name} {year}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    papers = []

    for entry in soup.find_all('li', class_='entry'):
        try:
            title_span = entry.find('span', class_='title')
            title = title_span.text.strip('. ') if title_span else 'N/A'

            authors = [a.text for a in entry.find_all('span', itemprop='author')]

            link_tag = entry.find('a', href=True, string='[doi]')
            link = link_tag['href'] if link_tag else 'N/A'

            papers.append({
                'title': title,
                'authors': ', '.join(authors),
                'year': year,
                'conference': conf_name,
                'link': link
            })
        except Exception as e:
            print(f"Error parsing paper in {conf_name} {year}: {e}")
            continue

    print(f"Successfully retrieved {len(papers)} papers for {conf_name} {year}")
    return papers

def retry_failed_scrapes():
    """
    Focuses only on the failed scrapes from the original run
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    try:
        existing_df = pd.read_csv(RAW_DATA_PATH)
        existing_data = existing_df.to_dict('records')
    except FileNotFoundError:
        existing_data = []

    failed_conferences = [
        ('CVPR', 'cvpr', 2025),
        ('ICML', 'icml', 2025),
        ('KDD', 'kdd', 2025),
        ('AAAI', 'aaai', 2021),
        ('AAAI', 'aaai', 2022),
        ('AAAI', 'aaai', 2023),
        ('AAAI', 'aaai', 2024),
        ('AAAI', 'aaai', 2025)
    ]

    all_papers_data = existing_data.copy()

    for conf_name, conf_short_name, year in failed_conferences:
        papers = get_papers_for_conference_year(conf_name, conf_short_name, year)
        if papers:
            all_papers_data.extend(papers)
        time.sleep(3)

    if not all_papers_data:
        print("No data was retrieved in this retry attempt.")
        return

    df = pd.DataFrame(all_papers_data)
    df.to_csv(RAW_DATA_PATH, index=False, encoding='utf-8-sig')
    print(f"\nRetry completed. Data saved to '{RAW_DATA_PATH}'")

if __name__ == '__main__':
    retry_failed_scrapes()