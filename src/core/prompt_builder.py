# src/core/prompt_builder.py
import re
from src.core.util.logger import Logger
from config.settings import config
from src.core.util.chat_formatter import ChatFormatter


class PromptBuilder:
    def __init__(self):
        self.logger = Logger()
        self.personality = self.load_personality()
        

    def generate_prompt(self, question, history):
        self.logger.debug(f"Gerando prompt. Pergunta: {question}")
        prompt = ChatFormatter.format_instruction_prompt(self.personality, history, question)
        self.logger.debug(f"Prompt gerado:\n**************\n {prompt}\n***************")
        return prompt

    def clean_response(self, raw_response):
        response_cleaned = re.sub(r'###.*?(\n|$)', '', raw_response, flags=re.DOTALL).strip()
        response_cleaned = ' '.join(response_cleaned.split())
        self.logger.debug(f"Resposta limpa: {response_cleaned}")
        return response_cleaned

    def load_personality(self):
        self.logger.debug("Carregando personalidade.")
        personality = "Você é um assistente de IA especializado em TI, fornecendo respostas diretas e técnicas."
        try:
            with open(config.PERSONALITY_FILE, "r", encoding="utf-8") as f:
                personality = f.read().strip()
        except FileNotFoundError:
            self.logger.warning(f"Arquivo de personalidade {config.PERSONALITY_FILE} não encontrado")
        return f"Seu nome é {config.ASSISTANT_NAME}. {personality}"
