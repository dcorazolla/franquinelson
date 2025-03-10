import unittest
from unittest.mock import patch
from src.prompt_builder import PromptBuilder
from config import CONFIG

class TestPromptBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = PromptBuilder(debug=True)

    def test_should_generate_prompt_with_context_when_context_provided(self):
        prompt = self.builder.generate_prompt("Qual a hora atual?", context="14h")
        self.assertIn("Contexto anterior: 14h", prompt)
        self.assertIn("Pergunta: Qual a hora atual?", prompt)

    def test_should_clean_response_correctly_when_response_contains_internal_instructions(self):
        response = "Está ensolarado! 🌞 ### instruções internas"
        cleaned = self.builder.clean_response(response)
        self.assertEqual(cleaned, "Está ensolarado! 🌞")

if __name__ == '__main__':
    unittest.main()
