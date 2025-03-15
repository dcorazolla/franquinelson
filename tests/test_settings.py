import unittest
from config.settings import config

class TestConfig(unittest.TestCase):
    """ Testes para garantir que as configurações estão corretas """

    def test_config_values(self):
        """ Verifica se os valores das configurações são os esperados """
        self.assertEqual(config.MODEL_NAME, "TheBloke/Llama-2-7B-Chat-GGUF")
        self.assertTrue(config.USE_CPU)
        self.assertEqual(config.DEVICE, "cpu")
        self.assertEqual(config.CONTEXT_SIZE, 2048)
        self.assertTrue(config.AUTO_DOWNLOAD)

    def test_to_dict(self):
        """ Verifica se o método to_dict retorna um dicionário válido """
        config_dict = config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertIn("MODEL_NAME", config_dict)
        self.assertIn("DEVICE", config_dict)

if __name__ == "__main__":
    unittest.main()
