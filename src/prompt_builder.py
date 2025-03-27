import json
import re
from src.util.logger import Logger
from config.settings import config

class PromptBuilder:

    def __init__(self):
        self.logger = Logger()
        self.personality = self.load_personality()

    def generate_prompt(self, question, history):
        """Gera prompt para o modelo"""
        self.logger.debug(f"Gerando prompt. Pergunta: {question}")

        history_json = json.dumps(history, ensure_ascii=False, indent=2)

        prompt_parts = [
            f"Responda conforme personalidade a seguir. Nome: {config.ASSISTANT_NAME}; Personalidade: ",
            self.personality.replace("\n", " "),
            "Contexto da conversa em json:",
            history_json,
            f"\nPergunta: {question}\nResposta:"
        ]

        print(prompt_parts)

        prompt = " ".join(prompt_parts)
        self.logger.debug(f"Prompt gerado:\n**************\n {prompt}\n***************")
        return prompt
    
    def clean_response(self, raw_response):
        response_cleaned = re.sub(r'###.*?(\n|$)', '', raw_response, flags=re.DOTALL).strip()
        response_cleaned = ' '.join(response_cleaned.split())

        self.logger.debug(f"Resposta limpa: {response_cleaned}")
        return response_cleaned


    def load_personality(self):
        """Carrega a personalidade do assistente a partir do arquivo."""
        self.logger.debug("Carregando personalidade.")
        personality = "Você é um assistente de IA especializado em TI, fornecendo respostas diretas e técnicas."
        try:
            with open(config.PERSONALITY_FILE, "r", encoding="utf-8") as f:
                personality = f.read().strip()
        except FileNotFoundError:
            self.logger.warning(f"Arquivo de personalidade {config.PERSONALITY_FILE} não encontrado")
        return personality
