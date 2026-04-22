# CampusPal

CampusPal is an AI-powered campus assistant for APSIT. It combines a React chat widget, a FastAPI backend, Groq-hosted LLM responses, LangChain orchestration, and a FAISS vector database built from APSIT website pages, PDFs, CSV tables, and curated institute documents.

The assistant is designed to answer APSIT-specific questions about admissions, fees, courses, placements, faculty, contacts, institute facilities, and official documents. Responses are grounded in the local document collection and include source file names where possible.

## Features

- Floating React chat widget for APSIT queries.
- Quick action prompts for admissions, fees, placements, and courses.
- Persistent chat history using browser local storage.
- Light and dark mode support.
- Markdown rendering for assistant answers.
- FastAPI `/chat` endpoint with conversation history support.
- Retrieval-augmented generation using LangChain and FAISS.
- Hugging Face sentence-transformer embeddings.
- Groq LLM integration through `langchain-groq`.
- Curated document filtering to prioritize high-signal APSIT information.
- Docker setup for running the backend and frontend together.
- Deployment notes for Render and Vercel.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 19, Vite, Tailwind CSS, lucide-react, react-markdown |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| AI/RAG | LangChain, ChatGroq, FAISS, HuggingFaceEmbeddings |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Data | APSIT scraped text files, CSV tables, PDFs, FAISS vector indexes |
| Deployment | Docker, Docker Compose, Render, Vercel, Nginx |

## Project Structure

```text
CampusPal/
+-- backend.py                    # FastAPI app and /chat endpoint
+-- rag_chain_builder.py          # CampusPal RAG chain, retrieval, reranking, LLM calls
+-- ingest.py                     # Builds the curated FAISS vector index
+-- test_embeddings.py            # Simple embedding initialization check
+-- requirements.txt              # Python dependencies
+-- Dockerfile                    # Backend Docker image
+-- docker-compose.yml            # Backend + frontend container setup
+-- DEPLOYMENT.md                 # Extra deployment guide
+-- frontend/
|   +-- src/App.jsx               # Main chat widget UI
|   +-- src/index.css             # Tailwind and global styles
|   +-- package.json              # Frontend scripts and dependencies
|   +-- Dockerfile                # Frontend build and Nginx image
|   +-- nginx.conf                # Nginx config for serving the built app
+-- scraper/
|   +-- data/                     # Extracted APSIT text and CSV files
|   +-- apsit_documents/          # Downloaded APSIT PDFs
|   +-- main.py                   # Scraper entry point / notes
+-- vectorstore/
    +-- db_faiss/                 # Existing FAISS index
    +-- db_faiss_campus/          # Curated CampusPal FAISS index
```

## How It Works

1. APSIT pages, PDFs, and tables are stored under `scraper/data` and `scraper/apsit_documents`.
2. `ingest.py` loads selected high-signal `.txt` and `.csv` sources from `scraper/data`.
3. Documents are split into chunks using LangChain text splitters.
4. Chunks are embedded with `sentence-transformers/all-MiniLM-L6-v2`.
5. The vectors are saved into `vectorstore/db_faiss_campus`.
6. `backend.py` starts a FastAPI server and initializes the RAG chain on startup.
7. The React frontend sends user questions and recent chat history to `POST /chat`.
8. `rag_chain_builder.py` retrieves relevant APSIT chunks, reranks them, asks Groq for a grounded answer, and returns the answer with sources.

## Prerequisites

- Python 3.10 or newer.
- Node.js 18 or newer.
- npm.
- A Groq API key.
- Docker Desktop, optional for containerized usage.

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

`GROQ_MODEL` is optional. If it is not provided, the backend uses `llama-3.3-70b-versatile`.

For the frontend, create `frontend/.env` when running outside Docker:

```env
VITE_API_URL=http://localhost:8000
```

For production, set `VITE_API_URL` to the deployed backend URL without a trailing slash.

## Local Setup

From the project root:

```bash
pip install -r requirements.txt
```

If the curated FAISS index is missing or you want to rebuild it:

```bash
python ingest.py
```

Start the backend:

```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
```

In a second terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually:

```text
http://localhost:5173
```

The backend health endpoint is available at:

```text
http://localhost:8000
```

## API Reference

### `GET /`

Returns a simple backend status response.

Example response:

```json
{
  "status": "CampusPal backend running"
}
```

### `POST /chat`

Sends a user question to the CampusPal RAG assistant.

Example request:

```json
{
  "input": "What courses are offered at APSIT?",
  "chat_history": [
    {
      "role": "user",
      "content": "Tell me about APSIT."
    },
    {
      "role": "assistant",
      "content": "APSIT information..."
    }
  ]
}
```

Example response:

```json
{
  "answer": "CampusPal response with a Sources line."
}
```

## Running With Docker

Make sure `.env` exists in the project root and contains `GROQ_API_KEY`.

Build and start both services:

```bash
docker-compose up --build
```

Then open:

```text
Frontend: http://localhost
Backend:  http://localhost:8000
```

The compose file mounts `vectorstore` and `scraper` into the backend container so the FAISS index and source data can be reused.

## Deployment

### Backend on Render

Use these settings for a Render web service:

```text
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend:app --host 0.0.0.0 --port $PORT
```

Required environment variable:

```text
GROQ_API_KEY
```

Optional environment variable:

```text
GROQ_MODEL
```

### Frontend on Vercel

Use these settings:

```text
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Required environment variable:

```text
VITE_API_URL=https://your-render-backend-url
```

Do not include a trailing slash in `VITE_API_URL`.

More deployment notes are available in `DEPLOYMENT.md`.

## Data and Index Maintenance

The RAG system primarily uses `scraper/data` as its document source. The curated ingestion process prefers files related to:

- Admissions.
- Fees.
- Courses.
- Faculty.
- Placements.
- Contact information.
- Leadership.
- Campus facilities.
- Library and cells or committees.

It intentionally deprioritizes noisy or very large sources such as broad syllabus files, approval reports, affiliation documents, magazines, and calendars unless they are explicitly whitelisted.

To refresh the vector index after changing data files:

```bash
python ingest.py
```

This rebuilds:

```text
vectorstore/db_faiss_campus
```

## Useful Commands

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Check embedding model initialization:

```bash
python test_embeddings.py
```

Rebuild the curated vector database:

```bash
python ingest.py
```

Run backend locally:

```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

Run frontend locally:

```bash
cd frontend
npm run dev
```

Build frontend:

```bash
cd frontend
npm run build
```

Run full stack with Docker:

```bash
docker-compose up --build
```

## Troubleshooting

### `GROQ_API_KEY not found in .env`

Create a `.env` file in the project root and add your Groq API key.

### Frontend says it cannot connect to the backend

Confirm the backend is running at `http://localhost:8000`. Also check that `frontend/.env` contains:

```env
VITE_API_URL=http://localhost:8000
```

Restart the frontend after changing Vite environment variables.

### FAISS index is missing

Run:

```bash
python ingest.py
```

The backend can also build the curated FAISS index at startup if it does not exist, but rebuilding it manually makes failures easier to diagnose.

### First startup is slow

The first run may download the Hugging Face embedding model and initialize the FAISS index. Later runs should be faster.

### Docker port conflict

Stop any local process already using port `80` or `8000`, or change the port mapping in `docker-compose.yml`.

## Notes

- The backend currently allows all CORS origins for easier local testing. For production, restrict `allow_origins` in `backend.py` to the deployed frontend domain.
- The assistant is instructed to answer only from retrieved APSIT context. If the retrieved documents do not contain a fact, it should say that the exact detail was not found.
- The frontend stores chat history in browser local storage under `campuspal_chat_history`.
- Source labels in answers come from local file names in `scraper/data`.
