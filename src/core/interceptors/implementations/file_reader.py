import os
import re
from src.core.util.logger import Logger
from ..input_interceptor import InputInterceptor

class FileReaderInterceptor(InputInterceptor):
    """
    Intercepta comandos <readfile path="arquivo" /> e substitui pelo conteúdo do arquivo.
    """

    READFILE_PATTERN = r'<readfile\s+path="(.+?)"\s*/>'

    def __init__(self):
        self.logger = Logger()

    def applies(self, text: str) -> bool:
        return re.search(self.READFILE_PATTERN, text) is not None

    def process(self, text: str) -> str:
        matches = re.findall(self.READFILE_PATTERN, text)
        if matches:
            self.logger.info(f"Comando <readfile/> detectado.")
        for filepath in matches:
            filepath = filepath.strip()
            self.logger.debug(f"Solicitada leitura do arquivo: {filepath}")
            content = self._read_file(filepath)
            replacement = f"\n[INÍCIO DO ARQUIVO: {filepath}]\n{content.strip()}\n[FIM DO ARQUIVO]\n"
            text = text.replace(f'<readfile path="{filepath}" />', replacement)
        return text

    def _read_file(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            self.logger.warning(f"Arquivo não encontrado: {filepath}")
            return f"[Erro: Arquivo '{filepath}' não encontrado.]"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                self.logger.info(f"Arquivo '{filepath}' lido com sucesso.")
                return content
        except Exception as e:
            self.logger.error(f"Erro ao ler o arquivo '{filepath}': {e}")
            return f"[Erro ao ler o arquivo '{filepath}': {str(e)}]"
