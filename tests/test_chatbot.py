import unittest
from src.chatbot import chatbot

class TestChatbot(unittest.TestCase):
    """ Testes para garantir o funcionamento do chatbot """

    def test_response_format(self):
        """ Testa se a resposta gerada é uma string válida """
        response = chatbot.generate_response("O que é um firewall?")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)  # A resposta não deve estar vazia

    def test_assistant_name(self):
        """ Verifica se o nome do assistente está correto """
        self.assertEqual(chatbot.assistant_name, "Franquinelson")

    def test_personality_load(self):
        """ Testa se a personalidade foi carregada corretamente """
        self.assertIsInstance(chatbot.personality, str)
        self.assertGreater(len(chatbot.personality), 10)  # Deve conter um texto significativo

if __name__ == "__main__":
    unittest.main()
