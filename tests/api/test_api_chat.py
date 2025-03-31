from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

def test_chat_retorna_resposta():
    response = client.post("/chat/", json={"prompt": "Quem foi Albert Einstein?"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)

def test_chat_prompt_vazio():
    response = client.post("/chat/", json={"prompt": " "})
    assert response.status_code == 400
