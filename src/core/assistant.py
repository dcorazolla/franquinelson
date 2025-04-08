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
                response = self._prepare_response(request)
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
        self.actual_interation["pergunta"] = request
        request = self.prompt_builder.generate_prompt(request, self.chat_history)
        return request
        
    def _prepare_response(self, request: str, auto_depth: int = 0) -> str:
        """
        Gera e processa a resposta a partir de um prompt. Caso a resposta contenha
        um comando de autoexecução (##rerun##), o fluxo será reiniciado automaticamente.

        Args:
            request (str): Prompt inicial.
            auto_depth (int): Nível atual de autoexecução (limite para evitar loop).

        Returns:
            str: Resposta final (sem comandos de rerun).
        """
        if auto_depth > 3:
            self.logger.warning("Limite de autoexecuções alcançado. Ignorando rerun.")
            return "[Limite de autoexecuções excedido.]"

        response = self.model(
            request,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE
        )
        cleaned_response = self.prompt_builder.clean_response(response['choices'][0]['text'])
        self.actual_interation["resposta"] = cleaned_response

        result = self.interceptor_manager.run_output_interceptors(cleaned_response)

        # if result != cleaned_response:
        #     self.logger.debug("Executando rerun automático.")
        #     self.print_response(f"Executando automaticamente: {result}")
        #     return self.prepare_response(
        #         self._prepare_request(result),
        #         auto_depth=auto_depth + 1
        #     )

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

    def response(self, request: str) -> str:
        prepared_request = self._prepare_request(request)
        return self._prepare_response(prepared_request)