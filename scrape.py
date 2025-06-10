import requests 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from app import is_valid_url
import re 


class Scrape:
    def __init__(self, url):
        self.url = url
        self.is_valid_url(self.url)


    def is_valid_url(self, url):
        """Ensure the URL is valid and contains a scheme (http/https)."""
        parsed_url = urlparse(url)

        if not parsed_url.scheme:
            print(f"⚠️ Warning: No scheme detected in URL '{url}'. Adding 'https://'.")
            url = f"https://{url}"
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"🚨 Invalid URL: {url}")
        
    # Get ASIN from URL
    def get_asin(self):
        asin = None
        parsed_url = urlparse(self.url)
        if "amazon" in parsed_url.netloc:
            asin_matched = re.search(r'/dp/([A-Z0-9]{10})', parsed_url.path)
            if asin_matched:
                asin = asin_matched.group(1)
        return asin
    
    def create_new_url(self):
        base_url = "https://www.amazon.com/dp/"
        asin = self.get_asin()
        if asin:
            new_url = urlunparse(('https', 'www.amazon.com', f'/dp/{asin}', '', '', ''))
            return new_url
        else:
            raise ValueError("ASIN not found in the provided URL.")
        
    def scrape(self):
        try:
            new_url = self.create_new_url()
        except ValueError as e:
            print(f"Error creating new URL: {e}")
            return None
        
        try:
            response = requests.get(new_url)

            if response.status_code != 200:
                print(f"Error fetching the page: {response.status_code}")
                return None
            soup = BeautifulSoup(response.content, 'html.parser')
            product_data = {
                "title": soup.find(id="productTitle").get_text(strip=True) if soup.find(id="productTitle") else None,
                "description": soup.find(id="feature-bullets").get_text(strip=True) if soup.find(id="feature-bullets") else None,
                "category": soup.find("span", class_="a-list-item").get_text(strip=True) if soup.find("span", class_="a-list-item") else None,
                "color": None,  # Color extraction logic can be added here
                "size": None,   # Size extraction logic can be added here
                "count": None   # Count extraction logic can be added here
            }
            return product_data
        except requests.RequestException as e:
            print(f"Error during request: {e}")
            return None
    
    def run(self):
        product_data = self.scrape()
        if product_data:
            print("Product data scraped successfully:")
            for key, value in product_data.items():
                print(f"{key}: {value}")
        else:
            print("Failed to scrape product data.")


if __name__ == "__main__":
    url = input("Enter the product URL: ")
    scraper = Scrape(url)
    scraper.run()