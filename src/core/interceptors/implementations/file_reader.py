# src/core/interceptors/implementations/file_reader.py
import os
import re
from src.core.util.logger import Logger
from ..input_interceptor import InputInterceptor

class FileReaderInterceptor(InputInterceptor):
    """
    Interceptor responsável por identificar comandos especiais para leitura de arquivos
    embutidos no prompt e substituir esses comandos pelo conteúdo dos arquivos especificados.

    Padrão do comando:
        ##readfile: nome_do_arquivo##
    """

    READFILE_PATTERN = r"##readfile:\s*(.+?)##"

    def __init__(self):
        """
        Inicializa o interceptor com um logger para registrar eventos e mensagens.
        """
        self.logger = Logger()

    def applies(self, text: str) -> bool:
        """
        Determina se o texto contém o comando especial para leitura de arquivo.

        Args:
            text (str): Texto inserido pelo usuário.

        Returns:
            bool: True se o comando especial for encontrado, False caso contrário.
        """
        return re.search(self.READFILE_PATTERN, text) is not None

    def process(self, text: str) -> str:
        """
        Processa o texto substituindo comandos especiais pelo conteúdo dos arquivos solicitados.

        Args:
            text (str): Texto original contendo comandos especiais.

        Returns:
            str: Texto processado com o conteúdo dos arquivos inseridos.
        """
        matches = re.findall(self.READFILE_PATTERN, text)
        for filename in matches:
            content = self._read_file(filename.strip())
            replacement = f"\n[INÍCIO DO ARQUIVO: {filename}]\n{content.strip()}\n[FIM DO ARQUIVO]\n"
            text = text.replace(f"##readfile: {filename}##", replacement)
        return text

    def _read_file(self, filepath: str) -> str:
        """
        Realiza a leitura segura do arquivo especificado, com tratamento de exceções.

        Args:
            filepath (str): Caminho relativo ou absoluto do arquivo.

        Returns:
            str: Conteúdo do arquivo ou mensagem de erro caso falhe.
        """
        if not os.path.isfile(filepath):
            return f"[Erro: Arquivo '{filepath}' não encontrado.]"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"[Erro ao ler o arquivo '{filepath}': {str(e)}]"
