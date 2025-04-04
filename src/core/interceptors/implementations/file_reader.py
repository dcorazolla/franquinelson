# src/core/interceptors/implementations/file_reader.py
import os
import re
from src.core.util.logger import Logger
from ..input_interceptor import InputInterceptor

class FileReaderInterceptor(InputInterceptor):
    READFILE_PATTERN = r"##readfile:\s*(.+?)##"

    def __init__(self):
        self.logger = Logger()

    def applies(self, text: str) -> bool:
        return re.search(self.READFILE_PATTERN, text) is not None

    def process(self, text: str) -> str:
        matches = re.findall(self.READFILE_PATTERN, text)
        for filename in matches:
            content = self._read_file(filename.strip())
            replacement = f"\n[INÍCIO DO ARQUIVO: {filename}]\n{content.strip()}\n[FIM DO ARQUIVO]\n"
            text = text.replace(f"##readfile: {filename}##", replacement)
        return text

    def _read_file(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            return f"[Erro: Arquivo '{filepath}' não encontrado.]"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"[Erro ao ler o arquivo '{filepath}': {str(e)}]"
