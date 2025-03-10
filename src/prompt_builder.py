import re
from .utils.logger import log_debug

class PromptBuilder:
    def __init__(self, debug=False):
        self.debug = debug

    def generate_prompt(self, question, context=None):
        from config import CONFIG

        prompt_parts = [
            f"Você é {CONFIG['name']}, assistente especializado em tecnologia.",
            "Responda em português claro, objetivo e amigável, utilizando emoticons."
        ]

        if context:
            prompt_parts.append(f"Contexto anterior: {context}")

        prompt_parts.append(f"\nPergunta: {question}\nResposta:")

        prompt = " ".join(prompt_parts)
        log_debug(f"Prompt gerado: {prompt}", self.debug)
        return prompt

    def clean_response(self, response):
        response_cleaned = re.sub(r'###.*?(\n|$)', '', response, flags=re.DOTALL).strip()
        response_cleaned = ' '.join(response_cleaned.split())

        log_debug(f"Resposta limpa: {response_cleaned}", self.debug)
        return response_cleaned
