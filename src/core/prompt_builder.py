import json
import re
from src.core.util.logger import Logger
from config.settings import config
from src.core.interceptors.file_reader_interceptor import FileReaderInterceptor

class PromptBuilder:

    def __init__(self):
        self.logger = Logger()
        self.personality = self.load_personality()
        self.interceptors = [
            FileReaderInterceptor()
        ]

    def generate_prompt(self, question, history):
        """Gera prompt para o modelo"""
        self.logger.debug(f"Gerando prompt. Pergunta: {question}")

        history_json = json.dumps(history, ensure_ascii=False, indent=2)
        personality_prepared = self.personality.replace("\n", " ")

        question_intercepted = self.intercept_prompt(question)

        prompt_parts = [
            f"Seu nome é {config.ASSISTANT_NAME}. {personality_prepared}",
            "Contexto da conversa em json:",
            history_json,
            f"\nPergunta: {question_intercepted}\nResposta:"
        ]

        prompt = " ".join(prompt_parts)
        self.logger.debug(f"Prompt gerado:\n**************\n {prompt}\n***************")
        return prompt
    
    def intercept_prompt(self, prompt):
        """Executa os interceptors de prompt"""
        self.logger.debug("Rodando interceptors de prompt")
        for interceptor in self.interceptors:
            prompt = interceptor.process(prompt)
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
