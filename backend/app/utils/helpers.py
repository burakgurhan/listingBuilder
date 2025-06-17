import validators
from urllib.parse import urlparse
from typing import Optional

def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, validators.url(url)])
    except ValueError:
        return False

def sanitize_url(url: str) -> str:
    """Clean and normalize URL."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url