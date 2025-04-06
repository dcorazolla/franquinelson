# src/core/interceptors/manager.py
from .input_interceptor import InputInterceptor
from .output_interceptor import OutputInterceptor


class InterceptorManager:
    """
    Gerenciador responsável por registrar e executar interceptadores.

    Essa classe mantém listas separadas para interceptadores de entrada e saída,
    executando-os automaticamente durante o ciclo de interação do assistente.
    """

    def __init__(self):
        """
        Inicializa o gerenciador e carrega interceptadores padrão automaticamente.
        """
        self.input_interceptors: list[InputInterceptor] = []
        self.output_interceptors: list[OutputInterceptor] = []
        self._load_default_interceptors()

    def _load_default_interceptors(self):
        """
        Carrega automaticamente interceptadores padrões na inicialização.
        """
        from .implementations.file_reader import FileReaderInterceptor
        self.input_interceptors.append(FileReaderInterceptor())
        
        from .implementations.file_writer import FileWriterInterceptor
        from .implementations.self_invoke import SelfInvokeInterceptor
        self.output_interceptors.append(FileWriterInterceptor())
        self.output_interceptors.append(SelfInvokeInterceptor())

    def run_input_interceptors(self, text: str) -> str:
        """
        Executa todos interceptadores de entrada aplicáveis sobre o texto.

        Args:
            text (str): Texto original fornecido pelo usuário.

        Returns:
            str: Texto após ser processado pelos interceptadores.
        """
        for interceptor in self.input_interceptors:
            if interceptor.applies(text):
                text = interceptor.process(text)
        return text

    def run_output_interceptors(self, text: str) -> str:
        """
        Executa todos interceptadores de saída aplicáveis sobre o texto.

        Args:
            text (str): Texto gerado pelo assistente.

        Returns:
            str: Texto após ser processado pelos interceptadores.
        """
        for interceptor in self.output_interceptors:
            if interceptor.applies(text):
                text = interceptor.process(text)
        return text
