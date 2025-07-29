from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from sqlalchemy import LargeBinary
import os
from app.database import Base

USE_PGVECTOR = os.getenv("USE_PGVECTOR", "true").lower() == "true"

if USE_PGVECTOR:
    EmbeddingType = Vector(384)
else:
    EmbeddingType = LargeBinary  # or Text (store serialized embeddings for SQLite dev)

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String, unique=True, index=True)
    agent_id = Column(String, index=True)
    customer_id = Column(String)
    language = Column(String)
    start_time = Column(DateTime, index=True)
    duration_seconds = Column(Integer)
    transcript = Column(Text)
    agent_talk_ratio = Column(Float)
    customer_sentiment_score = Column(Float)
    embedding = Column(EmbeddingType)
