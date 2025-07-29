from pydantic import BaseModel

class AgentAnalytics(BaseModel):
    agent_id: str
    avg_sentiment: float
    avg_talk_ratio: float
    total_calls: int
