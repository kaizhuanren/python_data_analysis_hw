# scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os

from config import CONFERENCE_MAP, START_YEAR, RAW_DATA_PATH, DATA_DIR

def get_papers_for_conference_year(conf_name, conf_short_name, year):
    if conf_short_name.lower() == 'nips':
        if year >= 2019:
            path_year = f"neurips{year}"
        else:
            path_year = f"nips{year}"
        url = f"https://dblp.org/db/conf/nips/{path_year}.html"
    else:
        url = f"https://dblp.org/db/conf/{conf_short_name}/{conf_short_name}{year}.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 ...'
    }

    print(f"正在爬取: {conf_name} {year} (URL: {url})")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"爬取失败: {e}")
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
            print(f"解析某篇论文时出错: {e}")
            continue

    print(f"成功爬取 {len(papers)} 篇论文。")
    return papers

def scrape_all_conferences():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    all_papers_data = []
    current_year = datetime.now().year
    
    for conf_name, conf_short_name in CONFERENCE_MAP.items():
        for year in range(START_YEAR, current_year + 1):
            papers = get_papers_for_conference_year(conf_name, conf_short_name, year)
            if papers:
                all_papers_data.extend(papers)
            time.sleep(2)

    if not all_papers_data:
        print("未能爬取到任何数据，请检查网络或URL配置。")
        return

    df = pd.DataFrame(all_papers_data)
    df.to_csv(RAW_DATA_PATH, index=False, encoding='utf-8-sig')
    print(f"\n所有数据已爬取完毕，并保存至 '{RAW_DATA_PATH}'")

if __name__ == '__main__':
    scrape_all_conferences()