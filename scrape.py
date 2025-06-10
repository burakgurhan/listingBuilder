import re
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from urllib.parse import urlparse, urlunparse

class Scrape:
    def __init__(self, url: str):
        self.url = self._validate_url(url)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.timeout = 10

    def _validate_url(self, url: str) -> str:
        """Validate and normalize URL."""
        parsed_url = urlparse(url)
        
        if not parsed_url.scheme:
            logging.warning(f"No scheme detected in URL '{url}'. Adding 'https://'.")
            url = f"https://{url}"
            parsed_url = urlparse(url)
            
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid URL: {url}")
            
        return url

    def get_asin(self) -> Optional[str]:
        """Extract ASIN from Amazon URL."""
        parsed_url = urlparse(self.url)
        if "amazon" in parsed_url.netloc:
            asin_matched = re.search(r'/dp/([A-Z0-9]{10})', parsed_url.path)
            return asin_matched.group(1) if asin_matched else None
        return None

    def create_new_url(self) -> str:
        """Create clean Amazon URL from ASIN."""
        asin = self.get_asin()
        if not asin:
            raise ValueError("ASIN not found in the provided URL.")
        return urlunparse(('https', 'www.amazon.com', f'/dp/{asin}', '', '', ''))

    def _extract_description(self, soup: BeautifulSoup) -> list:
        """Extract product description with multiple fallbacks."""
        description = []
        
        # Try feature bullets first
        feature_bullets = soup.find("div", id="feature-bullets")
        if feature_bullets:
            description = [li.get_text(strip=True) for li in feature_bullets.find_all("li")
                         if li.get_text(strip=True)]
            
        # Fallback to product description
        if not description:
            desc_div = soup.find("div", id="productDescription")
            if desc_div:
                description = [p.get_text(strip=True) for p in desc_div.find_all("p")
                             if p.get_text(strip=True)]
                
        return description

    def scrape(self) -> Optional[Dict[str, Any]]:
        """Scrape product data from Amazon."""
        try:
            new_url = self.create_new_url()
            response = requests.get(
                new_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                "title": (soup.find(id="productTitle").get_text(strip=True)
                         if soup.find(id="productTitle") else None),
                "description": self._extract_description(soup),
                "category": (soup.find("a", class_="a-link-normal a-color-tertiary").get_text(strip=True)
                            if soup.find("a", class_="a-link-normal a-color-tertiary") else None),
                "color": None,
                "size": None,
                "count": None
            }
            
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None
        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            return None

    def run(self) -> Optional[Dict[str, Any]]:
        """Execute the scraping process."""
        product_data = self.scrape()
        if product_data:
            logging.info("Product data scraped successfully")
            return product_data
        logging.error("Failed to scrape product data")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        url = input("Enter the product URL: ")
        scraper = Scrape(url)
        result = scraper.run()
        if result:
            for key, value in result.items():
                print(f"{key}: {value}")
    except Exception as e:
        logging.error(f"Script failed: {e}")