import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import concurrent.futures
import faker
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.call import Call
from app.services.ai import compute_embedding, compute_sentiment, compute_talk_ratio
from app.services.ingestion import generate_synthetic_transcript

fake = faker.Faker()

def ingest_one():
    try:
        transcript = generate_synthetic_transcript()
        with SessionLocal() as db:
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
        print(f"Inserted call_id: {call.call_id}")
    except Exception as e:
        print(f"Failed to ingest a call: {e}")


def main():
    # Use ThreadPoolExecutor for parallel execution of sync tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:  # Adjust workers as needed
        futures = [executor.submit(ingest_one) for _ in range(200)]
        concurrent.futures.wait(futures)  # Wait for all to complete

if __name__ == "__main__":
    main()
