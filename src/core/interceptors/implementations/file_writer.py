import os
import re
from src.core.util.logger import Logger
from ..output_interceptor import OutputInterceptor

class FileWriterInterceptor(OutputInterceptor):
    """
    Interceptor de saída que identifica comandos especiais para escrita em arquivo
    e executa a operação no sistema de arquivos.

    Padrão suportado:
        ##writefile: nome_do_arquivo # conteúdo ##
    """

    WRITEFILE_PATTERN = r"##writefile:\s*(.+?)\s*#\s*(.*?)\s*##"

    def __init__(self):
        self.logger = Logger()

    def applies(self, text: str) -> bool:
        """
        Verifica se o texto contém comandos de escrita de arquivo.

        Args:
            text (str): Saída do modelo.

        Returns:
            bool: True se houver comandos encontrados.
        """
        return re.search(self.WRITEFILE_PATTERN, text, re.DOTALL) is not None

    def process(self, text: str) -> str:
        """
        Processa o texto, executando as escritas de arquivos encontradas.

        Args:
            text (str): Saída original.

        Returns:
            str: Texto sem os comandos especiais de escrita.
        """
        matches = re.findall(self.WRITEFILE_PATTERN, text, re.DOTALL)
        for filename, content in matches:
            filename = filename.strip()
            content = content.strip()
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                self.logger.info(f"Arquivo '{filename}' escrito com sucesso.")
            except Exception as e:
                self.logger.error(f"Erro ao escrever arquivo '{filename}': {e}")
        return re.sub(self.WRITEFILE_PATTERN, '', text, flags=re.DOTALL).strip()
