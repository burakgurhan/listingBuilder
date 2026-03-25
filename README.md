# Listing Builder

An AI-powered application to dynamically generate e-commerce product listings by analyzing competitor URLs. 

## Tech Stack
- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Backend**: FastAPI (Python 3.11+) + SQLAlchemy 2.0 (SQLite)
- **AI Core**: CrewAI with Groq / OpenAI LLMs

## Setup & Execution

### Prerequisites
- Docker & Docker Compose
- API Keys (`OPENAI_API_KEY` and `GROQ_API_KEY`)

### Using Docker (Recommended for Production/Easy Start)
1. Create a `.env` file in the root directory based on the following:
   ```env
   OPENAI_API_KEY=your_openai_key_here
   GROQ_API_KEY=your_groq_key_here
   ```
2. Build and start the services using docker-compose:
   ```bash
   docker-compose up --build
   ```
3. Visit `http://localhost:3000` to access the application.

### Running Locally (For Development)

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# To run effectively, you should export PYTHONPATH
PYTHONPATH=. alembic upgrade head
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Features Complete
- **Modern Backend API**: Standardized FastAPI routing with SQLAlchemy 2.0 pattern.
- **Background Tasks Execution**: Long-running CrewAI processes are managed in background workers to avoid timeouts.
- **Frontend Dashboard Tooling**: User-friendly UI polling architecture to keep the client updated with AI generation results.
- **Persistent Storage**: Save historical jobs locally in a SQLite database via Alembic migrations.