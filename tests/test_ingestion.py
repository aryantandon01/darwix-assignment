from app.services.ingestion import generate_synthetic_transcript

def test_generate_transcript():
    transcript = generate_synthetic_transcript()
    assert isinstance(transcript, str)
    assert len(transcript) > 0
