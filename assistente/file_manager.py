import os
from .debug import log_debug

def criar_arquivo(nome_arquivo, conteudo, pasta="projetos"):
    caminho = os.path.expanduser(f"~/{pasta}/{nome_arquivo}")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        log_debug(f"Arquivo criado: {caminho}")
        return f"Arquivo criado: {caminho}"
    except Exception as e:
        log_debug(f"Erro ao criar arquivo {nome_arquivo}: {str(e)}")
        return f"Erro ao criar arquivo: {str(e)}"
