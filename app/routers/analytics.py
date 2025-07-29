from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.call import Call
from app.schemas.analytics import AgentAnalytics

router = APIRouter()

@router.get("/analytics/agents", response_model=List[AgentAnalytics])
def get_agent_analytics(db: Session = Depends(get_db)):
    results = (
        db.query(
            Call.agent_id,
            func.avg(Call.customer_sentiment_score).label("avg_sentiment"),
            func.avg(Call.agent_talk_ratio).label("avg_talk_ratio"),
            func.count(Call.id).label("total_calls")
        )
        .group_by(Call.agent_id)
        .all()
    )
    return [AgentAnalytics(agent_id=r.agent_id, avg_sentiment=r.avg_sentiment, avg_talk_ratio=r.avg_talk_ratio, total_calls=r.total_calls) for r in results]
