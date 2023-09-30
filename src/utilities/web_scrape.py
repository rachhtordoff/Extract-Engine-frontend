import requests
from bs4 import BeautifulSoup


def site_scrape(urls_list):
    websites_content = {}

    for url in urls_list:
        content = fetch_content(url)
        soup = BeautifulSoup(content, 'html.parser')
        # Get only the text content without HTML tags
        text_content = soup.get_text()
        websites_content[url] = text_content.strip()
    return websites_content

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

