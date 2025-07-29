from pydantic import BaseModel
from datetime import datetime

class CallResponse(BaseModel):
    call_id: str
    agent_id: str
    start_time: datetime
    customer_sentiment_score: float

    class Config:
        orm_mode = True

class CallDetail(BaseModel):
    call_id: str
    agent_id: str
    customer_id: str
    language: str
    start_time: datetime
    duration_seconds: int
    transcript: str
    agent_talk_ratio: float
    customer_sentiment_score: float

    class Config:
        orm_mode = True
