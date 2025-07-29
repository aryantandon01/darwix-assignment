from fastapi import APIRouter, HTTPException
from app.database import async_session
from app.models import Call
from app.schemas import RecommendationsResponse
from openai import OpenAI
import os

router = APIRouter(prefix="", tags=["recommendations"])

async def generate_coaching_nudges(transcript: str) -> list[str]:
    api_key = os.getenv("PERPLEXITY_API_KEY")  # Or OPENAI_API_KEY
    if not api_key:
        return ["Nudge 1 (mock): Review product details before call.",
                 "Nudge 2 (mock): Encourage customer questions.",
                 "Nudge 3 (mock): Practice closing techniques."]

    # Example using Perplexity
    client = Perplexity(api_key=api_key)
    prompt = f"""Based on this sales call transcript, provide three concise coaching tips for the agent, each 40 words or less:

    {transcript}

    Return only the tips, bulleted, without extra commentary."""
    
    response = client.chat.completions.create(
        model="llama-3-70b-instruct",  # Or another model
        messages=[
            {"role": "system", "content": "You are a helpful coach for sales professionals."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
    )
    # Parse bullets or newlines from response.choices[0].message.content
    nudges = response.choices[0].message.content.split('\n- ')[1:4]  # Adjust parsing as needed
    return [n[:120].strip() for n in nudges]  # Truncate for length

@router.get("/{call_id}/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(call_id: str):
    async with async_session() as db:
        call = await db.get(Call, call_id)
        if call is None:
            raise HTTPException(404, detail="Call not found")
        nudges = await generate_coaching_nudges(call.transcript)
        # ... get closest calls by cosine similarity (as before)
        return {"closest_calls": [...], "coaching_nudges": nudges}
