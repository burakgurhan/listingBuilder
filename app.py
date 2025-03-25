import streamlit as st
from main import SEOCrew
from urllib.parse import urlparse

# App configuration
st.set_page_config(
    page_title = "SEO Content Crew",
    page_icon="📝",
    layout = "centered",
)


def is_valid_url(url:str)->bool:
    """Check if a URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def run_seo_crew(url:str)->None:
    """Initialize and run the SEO Crew."""
    with st.status("🚀 Running SEO Crew...", expanded=True) as status:
        try:
            st.write("🔍 Initializing crew agents...")
            crew = SEOCrew(url).create_crew()

            if crew is None:
                st.error("Failed to initialize SEO Crew...")
                return
            
            st.write("📋 Starting tasks execution...")
            result = crew.kickoff()

            status.update(label="✅ SEO tasks completed!", state="complete")
            st.success("SEO Process completed successfully!")
            st.subheader("Results:")
            st.write("Title:")
            st.write(result["title"])
        
            st.write("Description:")
            st.write(result["description"])

        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

def main():
    st.title("📝 SEO Content Crew")
    st.markdown(""""
                This application uses AI agents to analyze your product URL and generate SEO-optimized content.
                """)
    
    with st.form("url_input_form"):
        url = st.text_input(
            "Enter a valid Amazon product URL:",
            placeholder="https://example.com/product",
            help="Please enter a valid HTTP/HTTPS URL"
        )

        submitted = st.form_submit_button("Run SEO Analysis")

        if submitted:
            if not url:
                st.warning("PLease enter a URL")
            elif not is_valid_url(url):
                st.error("Please enter a valid URL")
            else:
                run_seo_crew(url)

if __name__ == "__main__":
    main()
