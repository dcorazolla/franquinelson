import re
from tqdm import tqdm
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

        with tqdm(total=1, desc="Gerando prompt", unit="prompt") as progress_bar:
            prompt = " ".join(prompt_parts)
            progress = len(prompt_parts)
            progress += 1
            progress_bar.update(progress)

        log_debug(f"Prompt gerado: {prompt}", self.debug)
        return prompt

    def clean_response(self, response):
        with tqdm(total=2, desc="Limpando resposta") as progress_bar:
            response_cleaned = re.sub(r'###.*?(\n|$)', '', response, flags=re.DOTALL).strip()
            progress_bar.update(1)

            response_cleaned = ' '.join(response_cleaned.split())
            progress_bar.update(1)

        log_debug(f"Resposta limpa: {response_cleaned}", self.debug)
        return response_cleaned
