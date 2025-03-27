import logging
import inspect
from config.settings import config

class Logger:

    def __init__(self):
        """Inicializa o logger padrão do assistente"""

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
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)

