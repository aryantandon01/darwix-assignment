import asyncio
import faker
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.call import Call
from app.services.ai import compute_embedding, compute_sentiment, compute_talk_ratio
from app.services.ingestion import generate_synthetic_transcript

fake = faker.Faker()

async def ingest_one(db: Session):
    transcript = generate_synthetic_transcript()
    call = Call(
        call_id=fake.uuid4(),
        agent_id=fake.uuid4(),
        customer_id=fake.uuid4(),
        language="en",
        start_time=datetime.now() - timedelta(days=fake.random_int(1, 30)),
        duration_seconds=fake.random_int(60, 600),
        transcript=transcript,
        agent_talk_ratio=compute_talk_ratio(transcript),
        customer_sentiment_score=compute_sentiment(transcript),
        embedding=compute_embedding(transcript)
    )
    db.add(call)
    db.commit()

async def main():
    async with engine.begin() as conn:
        db = SessionLocal(bind=conn)
        tasks = [ingest_one(db) for _ in range(200)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
