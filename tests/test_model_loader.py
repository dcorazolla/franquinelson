import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.model_loader import ModelLoader
from config import CONFIG

class TestModelLoader(unittest.TestCase):

    @patch("os.path.isfile")
    def test_should_return_true_when_model_exists_given_file_exists(self, mock_isfile):
        mock_isfile.return_value = True
        loader = ModelLoader(debug=True)
        self.assertTrue(loader.model_exists())

    @patch("requests.get")
    def test_should_download_model_successfully_when_url_is_valid(self, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'data']
        mock_response.headers = {'content-length': '4'}
        mock_get.return_value = mock_response

        with patch("builtins.open", new_callable=mock_open) as mock_file:
            loader = ModelLoader(debug=True)
            loader.download_model()

            mock_get.assert_called_once_with(CONFIG['model']['url'], stream=True, timeout=300)
            mock_file = mock_file = mock_file().__enter__()
            mock_file.write.assert_called_with(b'data')

    @patch("llama_cpp.Llama", autospec=True)  # Evita carregar o modelo real
    @patch("os.path.isfile", return_value=True)
    def test_should_load_model_successfully_when_model_exists(self, mock_exists, mock_llama):
        loader = ModelLoader(debug=True)

        # Criamos um mock do modelo carregado
        mock_model_instance = MagicMock()
        mock_llama.return_value = mock_model_instance  # Quando chamado, retorna o mock

        model_instance = loader.load_model()

        # 🔥 Correção: Agora verificamos se `mock_llama()` foi chamado corretamente
        mock_llama.assert_called_once()

        self.assertEqual(model_instance, mock_model_instance)

if __name__ == '__main__':
    unittest.main()
