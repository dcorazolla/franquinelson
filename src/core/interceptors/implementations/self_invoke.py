import re
from src.core.util.logger import Logger
from ..output_interceptor import OutputInterceptor

class SelfInvokeInterceptor(OutputInterceptor):
    """
    Intercepta o bloco <rerun>nova_instrução</rerun> e executa a nova instrução como input.
    """

    PATTERN = r"<rerun>(.*?)</rerun>"

    def __init__(self):
        self.logger = Logger()

    def applies(self, text: str) -> bool:
        return re.search(self.PATTERN, text, re.DOTALL) is not None

    def process(self, text: str) -> str:
        match = re.search(self.PATTERN, text, re.DOTALL)
        self.logger.info(f"Comando <rerun/>: {text}") if match else None
        if match:
            nova_instrucao = match.group(1).strip()
            self.logger.info("Autoexecução detectada via <rerun>.")
            return nova_instrucao
        return text
