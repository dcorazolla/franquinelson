import os
import re
from src.core.util.logger import Logger
from ..output_interceptor import OutputInterceptor

class FileWriterInterceptor(OutputInterceptor):
    """
    Intercepta blocos <writefile name="arquivo">conteúdo</writefile> e cria o arquivo.
    """

    WRITEFILE_PATTERN = r'<writefile\s+path="(.+?)">(.*?)</writefile>'

    def __init__(self):
        self.logger = Logger()

    def applies(self, text: str) -> bool:
        return re.search(self.WRITEFILE_PATTERN, text, re.DOTALL) is not None

    def process(self, text: str) -> str:
        matches = re.findall(self.WRITEFILE_PATTERN, text, re.DOTALL)
        self.logger.info(f"Comando <writefile/> encontrado: {text}") if matches else None
        for filename, content in matches:
            try:
                with open(filename.strip(), "w", encoding="utf-8") as f:
                    f.write(content.strip())
                self.logger.info(f"Arquivo '{filename}' criado.")
            except Exception as e:
                self.logger.error(f"Erro ao escrever arquivo '{filename}': {e}")
        return re.sub(self.WRITEFILE_PATTERN, '', text, flags=re.DOTALL).strip()
