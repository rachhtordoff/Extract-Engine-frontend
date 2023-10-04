import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        self.websites_content = {}

    def site_scrape(self, urls_list):
        for url in urls_list:
            content = self.fetch_content(url)
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()
            self.websites_content[url] = text_content.strip()
        return self.websites_content

    def fetch_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching content from {url}: {e}")
            return ""
