import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.model_loader import ModelLoader

@pytest.fixture
def loader():
    return ModelLoader()

def test_model_exists_true(tmp_path):
    model_path = tmp_path / "modelo.gguf"
    model_path.write_text("fake model")
    with patch("src.model_loader.config.MODEL_FILE", str(model_path)):
        assert os.path.exists(model_path)

def test_model_exists_false(loader):
    with patch("os.path.exists", return_value=False):
        assert not loader._model_exists()

@patch("src.model_loader.requests.get")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("src.model_loader.tqdm")
def test_download_model(mock_tqdm, mock_makedirs, mock_open_file, mock_requests):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.headers = {"content-length": "100"}
    fake_response.iter_content = lambda chunk_size: [b"x" * 10] * 10
    mock_requests.return_value = fake_response

    loader = ModelLoader()
    with patch.object(loader, "_model_exists", return_value=False):
        loader.download_model()

@patch("src.model_loader.Llama")
@patch.object(ModelLoader, "_model_exists", return_value=True)
def test_load_model(mock_exists, mock_llama):
    loader = ModelLoader()
    model = loader.load_model()
    assert mock_llama.called

@patch("src.model_loader.requests.get")
@patch("src.model_loader.ModelLoader._model_exists", return_value=False)
def test_download_model_erro_http(mock_exists, mock_get):
    mock_get.return_value.status_code = 404
    loader = ModelLoader()
    with pytest.raises(RuntimeError):
        loader.download_model()

@patch("src.model_loader.requests.get")
@patch("src.model_loader.tqdm")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_download_model_sem_verbose(mock_makedirs, mock_open_file, mock_tqdm, mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.headers = {"content-length": "50"}
    fake_response.iter_content = lambda chunk_size: [b"x"] * 5
    mock_get.return_value = fake_response

    loader = ModelLoader()
    loader.verbose = False
    with patch.object(loader, "_model_exists", return_value=False):
        loader.download_model()

@patch("src.model_loader.requests.get", side_effect=Exception("conexão falhou"))
@patch.object(ModelLoader, "_model_exists", return_value=False)
def test_download_model_excecao_conexao(mock_exists, mock_get):
    loader = ModelLoader()
    with pytest.raises(Exception):
        loader.download_model()