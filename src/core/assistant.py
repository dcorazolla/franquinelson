# src/core/assistant.py
from config.settings import config
from .prompt_builder import PromptBuilder
from src.core.util.logger import Logger
from src.core.model_loader import ModelLoader
from src.core.interceptors.manager import InterceptorManager


class Assistant:

    def __init__(self):
        self.logger = Logger()
        self.logger.debug("Iniciando assistente")
        self.prompt_builder = PromptBuilder()
        self.model = ModelLoader().load_model()
        self.interceptor_manager = InterceptorManager()
        self.chat_history = []
        self.create_actual_interation()

    def chat(self) -> None:
        """Método principal de interação do assistente com o usuário"""
        print(f"{config.ASSISTANT_NAME} está online. Digite 'sair' para sair.")

        while True:
            user_input = input("\nVocê: ").strip()

            if user_input.lower() in ['exit', 'quit', 'sair', 'bye']:
                self.print_response("Até logo! 😊")
                break

            try:
                request = self._prepare_request(user_input)
                response = self.prepare_response(request)
                self.print_response(response)
            
            except ValueError as exception:
                self.print_response("Desculpe, tive um erro ao processar a questão.")
                
                if "exceed context window" in str(exception):
                    self.print_response("Limpando o histórico...")
                    self.history = []
                    self.print_response("Poderia repetir?")
                else:
                    raise exception
                
    def _prepare_request(self, request: str) -> str:
        """Prepara o input do usuário e executa os interceptors de input"""
        request = self.interceptor_manager.run_input_interceptors(request)
        print(self.actual_interation)
        self.actual_interation["pergunta"] = request
        request = self.prompt_builder.generate_prompt(request, self.chat_history)
        return request
        
    def prepare_response(self, request: str) -> str:
        response = self.model(
            request, 
            max_tokens=config.MAX_TOKENS, 
            temperature=config.TEMPERATURE
        )
        cleaned_response = self.prompt_builder.clean_response(response['choices'][0]['text'])
        self.actual_interation["resposta"] = cleaned_response;
        self.append_history()
        return cleaned_response
    
    def append_history(self):
        self.chat_history.append(self.actual_interation)
        self.create_actual_interation()
    
    def print_response(self, response: str) -> None:
        """Imprime mensagens com o nome do assistente"""
        print(f"\n{config.ASSISTANT_NAME}: {response}")

    def create_actual_interation(self):
        self.actual_interation = {"pergunta": "", "resposta": ""}