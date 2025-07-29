from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.call import Call
from app.schemas.call import CallResponse, CallDetail
from app.services.ai import get_similar_calls, generate_coaching_nudges
from sqlalchemy import func

router = APIRouter()

@router.get("/calls", response_model=List[CallResponse])
def get_calls(
    limit: int = 10, offset: int = 0, agent_id: str = None, from_date: datetime = None,
    to_date: datetime = None, min_sentiment: float = None, max_sentiment: float = None,
    db: Session = Depends(get_db)
):
    query = db.query(Call)
    if agent_id:
        query = query.filter(Call.agent_id == agent_id)
    if from_date:
        query = query.filter(Call.start_time >= from_date)
    if to_date:
        query = query.filter(Call.start_time <= to_date)
    if min_sentiment:
        query = query.filter(Call.customer_sentiment_score >= min_sentiment)
    if max_sentiment:
        query = query.filter(Call.customer_sentiment_score <= max_sentiment)
    return query.offset(offset).limit(limit).all()

@router.get("/calls/{call_id}", response_model=CallDetail)
def get_call_detail(call_id: str, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.get("/calls/{call_id}/recommendations")
def get_recommendations(call_id: str, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    similar = get_similar_calls(call.embedding, db, top_k=5)
    nudges = generate_coaching_nudges(call.transcript)
    return {"similar_calls": similar, "coaching_nudges": nudges}
