# ListingCrew: AI-Powered Listing Builder

ListingCrew is an AI-driven web application that automates the process of generating SEO-optimized product titles and descriptions for e-commerce listings. It leverages CrewAI agents to scrape product data, perform market research, and write compelling content.

## Features
- **Automated Web Scraping:** Extracts product details from URLs.
- **Market Research:** Identifies keywords, competitors, and trends.
- **SEO Content Generation:** Produces optimized titles and descriptions.
- **Streamlit UI:** Simple web interface for user input and results.
- **Configurable Agents:** Easily adjust agent behavior and LLM models via YAML files.

## Folder Structure
```
ListingCrew/
├── app.py           # Streamlit web app
├── crew.py          # CrewAI agent/task definitions
├── tools/
│   └── custom_tools.py
└── config/
    ├── agents.yaml
    └── tasks.yaml
```

## Getting Started

### Prerequisites
- Python 3.9+
- Streamlit
- CrewAI
- OpenAI and/or Groq API keys

### Installation
1. Navigate to the `ebayseoagents` root directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with API keys in the root directory:
   ```env
   OPENAI_API_KEY=your-openai-key
   GROQ_API_KEY=your-groq-key
   ```

### Running the App
From the `ebayseoagents` root directory:
```bash
streamlit run src/ListingCrew/app.py
```

## Usage
1. Enter a valid product URL in the web interface.
2. Click "Run Listing Builder".
3. View and copy the generated SEO title and description.

## Configuration
- **Agents and Tasks:**
  - Edit `src/ListingCrew/config/agents.yaml` and `tasks.yaml` to customize agent roles, goals, and LLM models.
- **Custom Tools:**
  - Add or modify validation logic in `src/ListingCrew/tools/custom_tools.py`.

## Troubleshooting
- Ensure your API keys are valid and set in `.env`.
- Check that your YAML config files are present and correctly formatted.
- For LLM errors, verify the `llm:` field uses the format `provider/model-id` (e.g., `openai/gpt-3.5-turbo`).

## License
MIT License

## Acknowledgements
- CrewAI
- Streamlit
- OpenAI
- Groq