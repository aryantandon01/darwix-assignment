from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector  # Requires pgvector extension for Postgres; fallback for SQLite

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String, unique=True, index=True)
    agent_id = Column(String, index=True)  # Indexed as per requirements
    customer_id = Column(String)
    language = Column(String)
    start_time = Column(DateTime, index=True)  # Indexed for date queries
    duration_seconds = Column(Integer)
    transcript = Column(Text)
    agent_talk_ratio = Column(Float)
    customer_sentiment_score = Column(Float)
    embedding = Column(Vector(384))  # For sentence-transformers/all-MiniLM-L6-v2 (384 dims)

# For full-text search: Use tsvector + GIN index.
# Rationale: GIN is efficient for composite searches on transcripts, faster than pg_trgm for large datasets.
# Add in migration: CREATE INDEX transcript_gin ON calls USING GIN(to_tsvector('english', transcript));
