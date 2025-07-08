import os
import json
from .crew import ListingCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def generate_listing(url: str) -> dict:
    """
    Run the ListingCrew and return the structured result as a dictionary.
    """
    inputs = {'url': url}
    crew_result = ListingCrew().crew().kickoff(inputs=inputs)

    # The writer task is the last one, and its output contains the structured data.
    # Accessing the specific task output is more reliable than using the crew's final raw output.
    # Assuming the writing task is the 3rd task (index 2).
    if crew_result.tasks_output and len(crew_result.tasks_output) > 2:
        writer_output_raw = crew_result.tasks_output[2].raw
        try:
            # The output from the writer agent is expected to be a JSON string.
            return json.loads(writer_output_raw)
        except (json.JSONDecodeError, TypeError):
            # Fallback if parsing fails, returning the raw string in a dict
            return {"raw_output": writer_output_raw}

    # Fallback to the crew's raw output if task-specific output isn't available for some reason.
    return {"raw_output": str(crew_result.raw)}

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