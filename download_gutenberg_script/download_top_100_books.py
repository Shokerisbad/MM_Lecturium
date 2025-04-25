import requests
from bs4 import BeautifulSoup
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Constants
TOP_100_URL = 'https://www.gutenberg.org/browse/scores/top'
DOWNLOAD_DIR = 'gutenberg_top_100'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetch_top_100_book_ids():
    response = requests.get(TOP_100_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    ol = soup.find('h2', string='Top 100 EBooks yesterday').find_next_sibling('ol')
    book_ids = []
    for li in ol.find_all('li'):
        link = li.find('a')
        if link and '/ebooks/' in link['href']:
            book_id = link['href'].split('/')[-1]
            book_ids.append((book_id, link.text.strip()))
    return book_ids

def download_book(book_id, title):
    base_url = f'https://www.gutenberg.org/ebooks/{book_id}'
    response = requests.get(base_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    epub_link = None
    txt_link = None
    for link in links:
        href = link['href']
        if href.endswith('.epub.images') or href.endswith('.epub.noimages'):
            epub_link = href
        elif href.endswith('.txt') or href.endswith('.txt.utf-8'):
            txt_link = href
    if epub_link:
        epub_url = f'https://www.gutenberg.org{epub_link}'
        epub_response = requests.get(epub_url, headers=HEADERS)
        epub_path = os.path.join(DOWNLOAD_DIR, f'{title}_{book_id}.epub')
        with open(epub_path, 'wb') as f:
            f.write(epub_response.content)
    if txt_link:
        txt_url = f'https://www.gutenberg.org{txt_link}'
        txt_response = requests.get(txt_url, headers=HEADERS)
        txt_path = os.path.join(DOWNLOAD_DIR, f'{title}_{book_id}.txt')
        with open(txt_path, 'wb') as f:
            f.write(txt_response.content)
    time.sleep(1)  # Be polite to the server

def main():
    book_list = fetch_top_100_book_ids()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for book_id, title in book_list:
            executor.submit(download_book, book_id, title)

if __name__ == '__main__':
    main()
