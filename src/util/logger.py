# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

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

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

