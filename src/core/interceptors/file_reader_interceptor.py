import os
import platform
import re
from src.core.util.logger import Logger

class FileReaderInterceptor:
    READFILE_PATTERN = r"##readfile:\s*(.+?)##"

    def __init__(self):
        self.logger = Logger()

    def process(self, prompt: str) -> str:
        """Executa interceptor file_Reader"""
        self.logger.debug("Executando interceptor read file...")        
        matches = re.findall(self.READFILE_PATTERN, prompt)
        for filename in matches:
            content = self._read_file(filename.strip())
            prepared_content = f"\n[INÍCIO DO ARQUIVO: {filename}]\n{content.strip()}\n[FIM DO ARQUIVO]\n"
            prompt = prompt.replace(f"##readfile: {filename}##", prepared_content)
        return prompt

    def _read_file(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            return f"[Erro: Arquivo '{filepath}' não encontrado.]"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"[Erro ao ler o arquivo '{filepath}': {str(e)}]"
