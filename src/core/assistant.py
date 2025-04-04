# src/core/assistant.py
from config.settings import config
from .prompt_builder import PromptBuilder
from src.core.util.logger import Logger
from src.core.model_loader import ModelLoader
from src.core.interceptors.manager import InterceptorManager


class Assistant:
    """
    Classe principal responsável por gerenciar a interação entre o usuário e o assistente.

    Controla todo o fluxo de conversação, incluindo preparação de prompts,
    execução do modelo, interceptação de comandos e gestão do histórico.
    """

    def __init__(self):
        """
        Inicializa componentes essenciais do assistente, como o modelo, 
        gerenciador de interceptadores, histórico e gerador de prompts.
        """
        self.logger = Logger()
        self.logger.debug("Iniciando assistente")
        self.prompt_builder = PromptBuilder()
        self.model = ModelLoader().load_model()
        self.interceptor_manager = InterceptorManager()
        self.chat_history = []
        self.create_actual_interation()

    def chat(self) -> None:
        """
        Inicia o ciclo principal de interação, permitindo conversas contínuas com o usuário.

        Usuário pode sair digitando comandos específicos como 'sair', 'quit', ou 'exit'.
        """
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
        """
        Processa o input do usuário executando interceptadores e formatando o prompt.

        Args:
            request (str): Texto inserido pelo usuário.

        Returns:
            str: Prompt formatado e pronto para ser enviado ao modelo.
        """
        request = self.interceptor_manager.run_input_interceptors(request)
        print(self.actual_interation)
        self.actual_interation["pergunta"] = request
        request = self.prompt_builder.generate_prompt(request, self.chat_history)
        return request
        
    def prepare_response(self, request: str) -> str:
        """
        Gera resposta a partir do prompt preparado, executando o modelo carregado.

        Args:
            request (str): Prompt formatado enviado ao modelo.

        Returns:
            str: Resposta do assistente processada e limpa.
        """
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
        """
        Adiciona a interação atual ao histórico da conversa e cria nova interação vazia.
        """
        self.chat_history.append(self.actual_interation)
        self.create_actual_interation()
    
    def print_response(self, response: str) -> None:
        """
        Exibe a resposta do assistente na interface do usuário.

        Args:
            response (str): Texto a ser exibido ao usuário.
        """
        print(f"\n{config.ASSISTANT_NAME}: {response}")

    def create_actual_interation(self):
        """
        Inicializa uma nova interação vazia para armazenar perguntas e respostas atuais.
        """
        self.actual_interation = {"pergunta": "", "resposta": ""}