from unittest.mock import patch
import src.main as main_mod

@patch("src.main.Assistant")
def test_main_chama_chat(MockAssistant):
    mock_instance = MockAssistant.return_value
    main_mod.main()
    mock_instance.chat.assert_called_once()

def test_main_importado_sem_executar():
    # Simula importação como módulo
    assert callable(main_mod.main)
