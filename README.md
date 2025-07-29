# Darwix AI Assignment: Sales Call Analytics Microservice

## Overview
A Python microservice for ingesting sales-call transcripts, storing them in a database, generating AI insights (embeddings, sentiment, talk ratios), and serving via a FastAPI REST API.

## Setup
1. Clone the repo: `git clone https://github.com/aryantandon01/darwix-assignment.git`
2. Create and activate a virtual env: `python -m venv venv` and `.\venv\Scripts\activate` (Windows).
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set vars (e.g., `DATABASE_URL=sqlite:///dev.db`, `PERPLEXITY_API_KEY=your_key`).
5. Initialize DB: `alembic upgrade head`
6. Run ingestion: `python scripts/ingest.py` (generates 200+ synthetic transcripts).
7. Start the API: `uvicorn app.main:app --reload`

For Docker: `docker build -t darwix-assignment .` and `docker run -p 8000:8000 darwix-assignment`.

## API Examples
- List calls: `curl "http://localhost:8000/api/v1/calls?limit=10&offset=0&agent_id=some_id&min_sentiment=-0.5"`
- Get single call: `curl http://localhost:8000/api/v1/calls/some_call_id`
- Get recommendations: `curl http://localhost:8000/api/v1/calls/some_call_id/recommendations`
- Agent analytics: `curl http://localhost:8000/api/v1/analytics/agents`

## Design Notes
- **Tech Choices**: FastAPI for async API, SQLAlchemy/Alembic for ORM/migrations, transformers for lightweight embeddings (all-MiniLM-L6-v2), Perplexity API for nudges/transcripts.
- **Indexing Rationale**: GIN on tsvector for efficient full-text search on transcripts (handles fuzzy/composite queries well); indexes on agent_id/start_time for fast filtering.
- **Error Handling**: Pydantic for validation, try/except in services for API faults (e.g., Perplexity errors fallback to samples).
- **Scaling**: ThreadPool for concurrent ingestion; could add Celery for background jobs under high load.
- **Assumptions/Trade-offs**: Synthetic data via Faker/Perplexity (no external dataset); SQLite for local dev (switch to Postgres in prod); cached AI results in DB to avoid recompute.

Licenses: No external datasets used; all synthetic.
