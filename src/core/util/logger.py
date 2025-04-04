# src/core/util/logger.py
import logging
import inspect
from config.settings import config

class Logger:
    """
    Classe utilitária para registro padronizado e estruturado de logs.

    Facilita a criação de logs detalhados, identificando automaticamente
    o nome da classe que utiliza o logger e centralizando a configuração dos níveis e formato.
    """

    def __init__(self):
        """
        Inicializa o logger configurando automaticamente o nome do logger com base na classe que o chama.
        """

        caller_class = inspect.stack()[1].frame.f_locals.get("self", None)
        logger_name = caller_class.__class__.__name__ if caller_class else "app"

        self.logger = logging.getLogger(logger_name)
        if not self.logger.hasHandlers():
            logging.basicConfig(
                encoding="utf-8",
                level=config.LOG_LEVEL,
                format="%(asctime)s (%(levelname)s) [%(name)s] - %(message)s"
            )
            self.logger.setLevel(config.LOG_LEVEL)

    def debug(self, message: str, *args, **kwargs):
        """Registra mensagem de debug (detalhes internos e técnicos)."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Registra mensagem informativa sobre processos normais."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Registra mensagem de aviso sobre condições não ideais."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Registra mensagem de erro sobre falhas que afetam parcialmente o funcionamento."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Registra mensagem crítica sobre falhas graves que comprometem totalmente o funcionamento."""
        self.logger.critical(message, *args, **kwargs)

