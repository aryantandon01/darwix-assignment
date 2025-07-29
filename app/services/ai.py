import os
from typing import List
import numpy as np
from transformers import AutoTokenizer, AutoModel, pipeline
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models.call import Call
import torch
import torch.nn.functional as F

# Perplexity client setup
PERPLEXITY_MODEL = "sonar-medium-online"
PERPLEXITY_BASE_URL = "https://api.perplexity.ai/"
client = (OpenAI(api_key=os.getenv("PERPLEXITY_API_KEY"), base_url=PERPLEXITY_BASE_URL)
          if os.getenv("PERPLEXITY_API_KEY") else None)

# Sentiment pipeline - Use a public model to avoid auth issues (alternative: login and use default "sentiment-analysis")
sentiment_pipeline = pipeline("sentiment-analysis")

# Load tokenizer and model directly with transformers
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def compute_embedding(transcript: str) -> np.ndarray:
    """Generate a sentence embedding using transformers directly."""
    # Tokenize
    encoded_input = tokenizer([transcript], padding=True, truncation=True, return_tensors='pt')
    
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    # Mean pooling
    attention_mask = encoded_input['attention_mask']
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    sentence_embeddings = sum_embeddings / sum_mask
    
    # Normalize
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
    
    return sentence_embeddings.cpu().numpy()[0]  # Return as numpy array for consistency

def compute_sentiment(transcript: str) -> float:
    """Compute sentiment score using Hugging Face pipeline."""
    result = sentiment_pipeline(transcript)[0]
    label = result['label'].upper()
    score = result['score']
    if label == 'POSITIVE':
        return score  # 0 to 1
    elif label == 'NEGATIVE':
        return -score  # -1 to 0
    return 0.0

def compute_talk_ratio(transcript: str) -> float:
    """Calculate agent talk ratio; exclude filler words (very rough)."""
    words = transcript.split()
    agent_words = len([w for w in words if w.lower() not in ['um', 'uh'] and 'Agent:' in transcript])
    total_words = len([w for w in words if w.lower() not in ['um', 'uh']])
    return agent_words / total_words if total_words > 0 else 0.0

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Manual cosine similarity using numpy."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_similar_calls(embedding: np.ndarray, db: Session, top_k: int = 5) -> List[str]:
    """Return top_k most similar calls by cosine similarity on embeddings."""
    calls = db.query(Call).all()
    similarities = [(c.call_id, cosine_similarity(embedding, c.embedding)) for c in calls if c.embedding is not None]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in similarities[:top_k]]

def generate_coaching_nudges(transcript: str) -> List[str]:
    """Generate 3 short coaching nudges using Perplexity API."""
    if not client:
        return ["Sample nudge 1", "Sample nudge 2", "Sample nudge 3"]
    try:
        response = client.chat.completions.create(
            model=PERPLEXITY_MODEL,
            messages=[
                {"role": "system", "content": "You are a call coach. Generate 3 short coaching tips (40 words or less each) for call transcripts."},
                {"role": "user", "content": f"Call transcript: {transcript}"},
            ],
            max_tokens=160,
            temperature=0.7,
        )
        nudges = response.choices[0].message.content.strip().split('\n')[:3]
        # In case Perplexity returns a single string, split by newlines, trim, and cap at 3 nudges
        return [n.strip() for n in nudges if n.strip()][:3]
    except Exception as e:
        print(f"Perplexity API error: {e}")
        return ["Coaching nudge generation failed."] * 3  # Graceful fallback
