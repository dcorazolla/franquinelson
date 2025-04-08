import pytest
from src.core.prompt_builder import PromptBuilder

@pytest.fixture
def builder():
    return PromptBuilder()

def test_load_personality_default(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *a, **kw: (_ for _ in ()).throw(FileNotFoundError()))
    builder = PromptBuilder()
    assert "assistente de IA" in builder.personality

def test_generate_prompt(builder):
    pergunta = "O que é Python?"
    history = [{"pergunta": "Oi", "resposta": "Olá!"}]
    prompt = builder.generate_prompt(pergunta, history)
    assert "Python" in prompt
    assert "### Conversa:" in prompt

def test_clean_response(builder):
    raw = "### Resposta\nIsso é um teste. ###"
    limpa = builder.clean_response(raw)
    assert "teste" in limpa
    assert "###" not in limpa
