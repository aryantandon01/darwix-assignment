from app.models.call import Call

def test_call_model():
    call = Call(call_id="test")
    assert call.call_id == "test"
