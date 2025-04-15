import logging
import validators
import streamlit as st
from main import SEOCrew
from urllib.parse import urlparse
import json 

# App configuration
st.set_page_config(
    page_title = "Listing Builder",
    page_icon="📝",
    layout = "centered",
)


def is_valid_url(url: str)->bool:
    """Check if a URL is valid."""
    try:
        result = urlparse(url)
        url_valid = validators.url(url)
        return all([result.scheme, result.netloc, url_valid])
    except ValueError:
        return False

# Set up logging
logging.basicConfig(level=logging.INFO)

def run_seo_crew(url: str) -> None:
    """Initialize and run the SEO Crew."""
    logging.info(f"URL received: {url}")
    with st.spinner("🚀 The crew building title and description..."):
        try:
            st.write("🔍 Initializing crew agents...")
            crew = SEOCrew(url).create_crew()
            if crew is None:
                st.error("Failed to initialize SEO Crew. Please check the API keys and input data.")
                return

            st.write("📋 Starting tasks execution...")
            result = crew.kickoff()
            logging.info("Title and description completed successfully.")
            st.success("Title and description completed successfully!")

            # Access attributes directly from the CrewOutput object
            try:
                seo_output = result.tasks_output[2].raw
                parsed_result = json.loads(seo_output)
                
                # Extract title and description
                title = parsed_result.get("title", "No title found")
                description = parsed_result.get("description", "No description found")

            except json.JSONDecodeError as e:
                st.error(f"Error parsing JSON response: {str(e)}")
                logging.error(f"JSONDecodeError: {str(e)}")
                return
            # Display the title and description
            st.subheader("📦 Product Details")
            st.markdown(f"**Title:** {title}")
            st.markdown(f"**Description:** {description}")

        except KeyError as e:
            st.error(f"Missing key in response: {str(e)}")
            logging.error(f"KeyError: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred during SEO Crew execution: {str(e)}")
            logging.exception(e)

def main():
    st.title("📝 Listing Builder")
    st.markdown("""
                This application uses AI agents to analyze your product URL and generate SEO-optimized title and description.
                """)
    
    with st.form("url_input_form"):
        url = st.text_input(
            "Enter a valid product URL:",
            placeholder="https://example.com/product",
            help="Please enter a valid HTTP/HTTPS URL"
        )

        submitted = st.form_submit_button("Run Listing Builder")

        if submitted:
            if not url:
                st.warning("Please enter a URL")
            elif not is_valid_url(url):
                st.error("Please enter a valid URL")
            else:
                run_seo_crew(url)

if __name__ == "__main__":
    main()
