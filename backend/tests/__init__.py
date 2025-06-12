import os
import sys
import pytest
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables for testing
load_dotenv()

# Test configuration
TEST_CONFIG = {
    'TEST_URL': 'https://www.ebay.co.uk/itm/sample',
    'TEST_ASIN': 'B08N5WRWNW',
    'TEST_TITLE': 'Sample Product Title',
    'TEST_DESCRIPTION': 'Sample product description for testing.',
}

# Pytest fixtures that can be used across all tests
@pytest.fixture
def sample_url():
    """Return a sample URL for testing."""
    return TEST_CONFIG['TEST_URL']

@pytest.fixture
def sample_product_data():
    """Return sample product data for testing."""
    return {
        'asin': TEST_CONFIG['TEST_ASIN'],
        'title': TEST_CONFIG['TEST_TITLE'],
        'description': TEST_CONFIG['TEST_DESCRIPTION']
    }

# Mock API responses
@pytest.fixture
def mock_api_response():
    """Return mock API response for testing."""
    return {
        'success': True,
        'data': {
            'title': TEST_CONFIG['TEST_TITLE'],
            'description': TEST_CONFIG['TEST_DESCRIPTION']
        }
    }