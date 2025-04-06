import re
from src.core.util.logger import Logger
from ..output_interceptor import OutputInterceptor

class SelfInvokeInterceptor(OutputInterceptor):
    """
    Intercepta o bloco <rerun>nova_instrução</rerun> e executa a nova instrução como input.
    """

    PATTERN = r"<rerun>(.*?)</rerun>"
    MAX_RERUNS = 3

    def __init__(self):
        self.logger = Logger()
        self.rerun_count = 0

    def applies(self, text: str) -> bool:
        return re.search(self.PATTERN, text, re.DOTALL) is not None

    def process(self, text: str) -> str:
        match = re.search(self.PATTERN, text, re.DOTALL)

        if match:
            if self.rerun_count >= self.MAX_RERUNS:
                self.logger.warning("Limite máximo de autoexecuções atingido. Ignorando <rerun>.")
                return re.sub(self.PATTERN, '', text, flags=re.DOTALL).strip()

            nova_instrucao = match.group(1).strip()
            self.logger.info(f"Autoexecução detectada via <rerun>: {nova_instrucao}")
            self.rerun_count += 1
            return nova_instrucao
        
        return text
    
    def reset(self):
        """ Reinicia a contagem de autoexecuções. Deve ser chamado no início de cada nova interação. """
        self.rerun_count = 0
