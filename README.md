# Darwix AI Assignment: Sales Call Analytics Microservice

## Overview  
This repository contains a Python microservice designed to ingest sales call transcripts, persist them in a database, generate AI-powered insights such as embeddings, sentiment scores, and agent talk ratios, and serve actionable analytics via a FastAPI REST API.

## Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone 
   cd aryantandon01-darwix-assignment
   ```

2. **Create and activate the Python virtual environment**  
   - Windows:  
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Unix/macOS:  
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**  
   - Copy `.env.example` to `.env` and fill in your keys:  
     - `DATABASE_URL` (default is SQLite local file)  
     - `PERPLEXITY_API_KEY` for AI calls  
   
5. **Apply database migrations**  
   ```bash
   alembic upgrade head
   ```

6. **Ingest synthetic data**  
   ```bash
   python scripts/ingest.py
   ```
   Runs ingestion of 200+ synthetic call transcripts with AI insights.

7. **Start the API server**  
   ```bash
   uvicorn app.main:app --reload
   ```
   The API is available at [`http://localhost:8000`](http://localhost:8000).

## API Usage Examples & Sample Outputs

Use the interactive Swagger UI at [`http://localhost:8000/docs`](http://localhost:8000/docs) or the commands below:

### 1. List calls  
**Request:**  
```bash
curl "http://localhost:8000/api/v1/calls?limit=10"
```

**Sample Response:**  
```json
[
  {
    "call_id": "e6043c38-2101-4981-bcf8-58786c9a39be",
    "agent_id": "b6862934-ca55-4363-b609-846feb02742d",
    "start_time": "2025-07-22T00:36:27.150531",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "77ab74f8-72c1-4c11-987d-2cbabc79d4c8",
    "agent_id": "b0665058-c57f-4a44-b979-212c53d04486",
    "start_time": "2025-07-01T00:36:27.157741",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "004c8a7f-7b70-4e16-8187-6f3cbbecd718",
    "agent_id": "7aeb5822-4c01-426a-9435-23887989c6db",
    "start_time": "2025-07-02T00:36:27.140849",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "8e4bfe0c-02c0-4e9e-a9d5-12155615ee23",
    "agent_id": "b84334ce-4758-4c83-bb4a-0065be91af59",
    "start_time": "2025-07-13T00:36:27.973364",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "3272a0b4-540b-4e32-81ac-42d3287a090c",
    "agent_id": "3243601c-f5c8-434f-a034-7a9fabc1f802",
    "start_time": "2025-07-04T00:36:27.149508",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "675d5fb3-adcd-4753-8923-5b75dc418255",
    "agent_id": "7b3edd27-12cf-464e-8cb0-492d7785457c",
    "start_time": "2025-07-12T00:36:27.148509",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "214c462c-1816-41f0-a457-38ac31891676",
    "agent_id": "4796f76a-e170-48e1-975d-68f2f23623e4",
    "start_time": "2025-07-19T00:36:28.141515",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "c6a704a9-f7a2-4b9c-a9c3-b6f4e670bc80",
    "agent_id": "72f56b0e-0dc4-4e24-b1ba-705a80ce60a2",
    "start_time": "2025-07-22T00:36:27.155776",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "0f37fbb4-d019-4ce0-850b-3902c9d10a56",
    "agent_id": "6de2470f-089d-4eb8-87dd-b2f1b7c1a4f3",
    "start_time": "2025-07-04T00:36:27.142718",
    "customer_sentiment_score": 0.9997119307518005
  },
  {
    "call_id": "b597ad5f-30f8-447a-9620-590a699405c3",
    "agent_id": "6b3489a6-c48c-462c-a52e-f43f0d537a7f",
    "start_time": "2025-07-08T00:36:28.603138",
    "customer_sentiment_score": 0.9997119307518005
  }
]
```

### 2. Get call detail  
**Request:**  
```bash
curl "http://localhost:8000/api/v1/calls/e6043c38-2101-4981-bcf8-58786c9a39be"
```

**Sample Response:**  
```json
{
  "call_id": "e6043c38-2101-4981-bcf8-58786c9a39be",
  "agent_id": "b6862934-ca55-4363-b609-846feb02742d",
  "customer_id": "6e32da32-fcc4-46ff-a39c-c01d9c69c973",
  "language": "en",
  "start_time": "2025-07-22T00:36:27.150531",
  "duration_seconds": 135,
  "transcript": "Agent: Hello, how can I help? Customer: I need info on product X. Agent: Sure, it's great!",
  "agent_talk_ratio": 1,
  "customer_sentiment_score": 0.9997119307518005
}
```

### 3. Get recommendations  
**Request:**  
```bash
curl "http://localhost:8000/api/v1/calls/e6043c38-2101-4981-bcf8-58786c9a39be/recommendations"
```

**Sample Response:**  
```json
{
  "similar_calls": [
    "e6043c38-2101-4981-bcf8-58786c9a39be",
    "77ab74f8-72c1-4c11-987d-2cbabc79d4c8",
    "004c8a7f-7b70-4e16-8187-6f3cbbecd718",
    "8e4bfe0c-02c0-4e9e-a9d5-12155615ee23",
    "3272a0b4-540b-4e32-81ac-42d3287a090c"
  ],
  "coaching_nudges": [
    "Sample nudge 1",
    "Sample nudge 2",
    "Sample nudge 3"
  ]
}
```

### 4. Get aggregated agent analytics  
**Request:**  
```bash
curl "http://localhost:8000/api/v1/analytics/agents"
```

**Sample Response:**  
```json
[
  {
    "agent_id": "030ae412-9795-4b43-840a-69101e8b0c1b",
    "avg_sentiment": 0.9997119307518005,
    "avg_talk_ratio": 1,
    "total_calls": 1
  },
  {
    "agent_id": "0379ef28-3e29-449f-8889-11500c932f47",
    "avg_sentiment": 0.9997119307518005,
    "avg_talk_ratio": 1,
    "total_calls": 1
  },
  {
    ....
  },
  ....
]
```

## Design Notes

- **Tech Stack:** FastAPI for asynchronous REST API; SQLAlchemy with Alembic for ORM and schema migrations; PostgreSQL (SQLite for local dev); transformers and Perplexity API for AI insights; Docker for containerization.
- **Data Ingestion:** Uses a thread pool for concurrent calls to generate 200 synthetic sales call transcripts with embeddings, sentiment, and talk ratios computed and stored.
- **Storage Layer:** Database schema optimized with indexes on `agent_id` and `start_time` for efficient filtering. Uses PostgreSQL GIN index on `tsvector` for full-text search over transcripts.
- **AI Module:** Embeddings computed with `all-MiniLM-L6-v2` transformer (mean pooling and normalization). Sentiment via Hugging Face pipeline mapped to a score between -1 and 1. Coaching nudges generated dynamically by Perplexity API for actionable agent feedback.
- **API Endpoints:** CRUD and analytics endpoints implemented with Pydantic models for request/response validation and consistent HTTP codes.
- **Testing:** Pytest tests cover ingestion logic, API endpoints, models, and AI service functions. Aim for 70% coverage.
- **CI/CD:** GitHub Actions workflow runs tests, types checks, linting, and Docker image build on push.
- **Containerization:** Dockerfile provided for easy deployment; optional `docker-compose.yml` supports local Postgres with API.
- **Assumptions:** Synthetic data used for privacy and simplicity; caching AI outputs to avoid redundant computation; error handling implemented for external API calls.

## Final Notes

- To re-run ingestion and refresh data:  
  ```bash
  python scripts/ingest.py
  ```

- Start the API server:  
  ```bash
  uvicorn app.main:app --reload
  ```

- Explore the interactive documentation and test all endpoints at:  
  [http://localhost:8000/docs](http://localhost:8000/docs)