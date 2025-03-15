import unittest
import os
from src.model_loader import model_loader
from config.settings import config

class TestModelLoader(unittest.TestCase):
    """ Testes para garantir que o modelo é carregado corretamente. """

    def test_model_file_exists(self):
        """ Testa se o modelo já foi baixado ou pode ser baixado corretamente. """
        model_loader.download_model()
        self.assertTrue(os.path.exists(config.MODEL_FILE))

    def test_load_model(self):
        """ Testa se o modelo é carregado sem erros. """
        model = model_loader.load_model()
        self.assertIsNotNone(model)

    def test_log_output(self):
        """ Testa se os logs de debug funcionam corretamente. """
        model_loader._log("Teste de log")
        self.assertTrue(True)  # Apenas verifica se não lança erro

if __name__ == "__main__":
    unittest.main()
