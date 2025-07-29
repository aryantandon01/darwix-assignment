from app.services.ai import compute_sentiment

def test_compute_sentiment():
    score = compute_sentiment("This is great!")
    assert -1 <= score <= 1
