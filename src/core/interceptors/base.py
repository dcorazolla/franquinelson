# src/core/interceptors/base.py
from abc import ABC, abstractmethod

class BaseInterceptor(ABC):
    """
    Classe abstrata base para interceptadores.

    Define o contrato padrão dos interceptadores utilizados para manipular
    entradas e saídas do assistente através de comandos especiais embutidos no prompt.
    """
    
    @abstractmethod
    def applies(self, text: str) -> bool:
        """
        Avalia se o interceptor deve ser aplicado ao texto fornecido.

        Args:
            text (str): O texto a ser avaliado.

        Returns:
            bool: True se o interceptor se aplica, False caso contrário.
        """
        pass

    @abstractmethod
    def process(self, text: str) -> str:
        """
        Executa o processamento do interceptor sobre o texto fornecido.

        Args:
            text (str): O texto a ser processado.

        Returns:
            str: O texto após processamento.
        """
        pass
