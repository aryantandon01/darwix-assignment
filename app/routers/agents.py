from fastapi import APIRouter
from sqlalchemy import func, select, and_
from app.database import async_session
from app.models import Call
from app.schemas import AgentsResponse

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("/", response_model=AgentsResponse)
async def get_agents():
    async with async_session() as db:
        stmt = (
            select(
                Call.agent_id,
                func.avg(Call.sentiment_score).label("avg_sentiment"),
                func.avg(Call.agent_talk_ratio).label("avg_talk_ratio"),
                func.count().label("call_count"),
            )
            .group_by(Call.agent_id)
        )
        result = await db.execute(stmt)
        agents = result.fetchall()
        return {"agents": agents}
