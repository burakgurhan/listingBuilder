import os
from crew import ListingCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def generate_listing(url: str) -> dict:
    """
    Run the ListingCrew and return the result as a dictionary.
    """
    inputs = {'url': url}
    result = ListingCrew().crew().kickoff(inputs=inputs)
    # Try to parse the result as dict, fallback to raw string
    try:
        return result.raw if isinstance(result.raw, dict) else {"raw": result.raw}
    except Exception:
        return {"raw": str(result.raw)}

def run():
    """
    CLI entry point for manual testing.
    """
    url = 'https://www.amazon.ca/Patella-Support-Basketball-Tendonitis-Volleyball/dp/B07DLFP8Q5/'
    result = generate_listing(url)
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result)
    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()