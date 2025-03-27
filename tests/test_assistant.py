from unittest.mock import patch, MagicMock
import builtins
from src.assistant import FranquinelsonAssistant
import pytest

@patch("src.assistant.ModelLoader")
def test_response_normal(MockModelLoader):
    MockModelLoader.return_value.load_model.return_value = lambda *a, **k: {
        "choices": [{"text": "Texto de resposta"}]
    }

    assistant = FranquinelsonAssistant()
    response = assistant.response("O que é memória RAM?")
    assert isinstance(response, str)

@patch("src.assistant.ModelLoader")
def test_respone_contexto_excedido(MockModelLoader):
    def raise_context_error(*a, **k):
        raise ValueError("exceed context window")
    
    MockModelLoader.return_value.load_model.return_value = raise_context_error
    assistant = FranquinelsonAssistant()

    try:
        assistant.response("Explique IA.")
    except ValueError as e:
        assert "context window" in str(e)

@patch("src.assistant.ModelLoader")
def test_response(MockModelLoader):
    MockModelLoader.return_value.load_model.return_value = lambda *a, **k: {
        "choices": [{"text": "Resposta simulada"}]
    }

    assistant = FranquinelsonAssistant()
    resposta = assistant.response("O que é CPU?")
    assert isinstance(resposta, str)

@patch("src.assistant.ModelLoader")
@patch("builtins.input", side_effect=["oi", "sair"])
@patch("builtins.print")
def test_chat(MockPrint, MockInput, MockModelLoader):
    MockModelLoader.return_value.load_model.return_value = lambda *a, **k: {
        "choices": [{"text": "Teste"}]
    }

    assistant = FranquinelsonAssistant()
    assistant.chat()

    # Verifica se chamou print com a resposta final
    MockPrint.assert_any_call("\nFranquinelson: Teste")

@patch("src.assistant.ModelLoader")
@patch("builtins.input", side_effect=["erro", "sair"])
@patch("builtins.print")
def test_chat_erro_generico(MockPrint, MockInput, MockModelLoader):
    def raise_erro(*a, **k):
        raise ValueError("erro qualquer")

    MockModelLoader.return_value.load_model.return_value = raise_erro

    assistant = FranquinelsonAssistant()
    with pytest.raises(ValueError):
        assistant.chat()
