import os
from src.core.interceptors.implementations.file_writer import FileWriterInterceptor

def test_writefile_cria_arquivo(tmp_path):
    caminho = tmp_path / "saida.txt"
    entrada = f"<writefile path=\"{caminho}\">conteúdo gravado</writefile>"

    interceptor = FileWriterInterceptor()
    saida = interceptor.process(entrada)

    assert not "<writefile" in saida
    assert caminho.exists()
    assert caminho.read_text(encoding="utf-8") == "conteúdo gravado"

def test_writefile_falha_permissao(monkeypatch):
    def simula_erro(*args, **kwargs):
        raise IOError("falha simulada")

    interceptor = FileWriterInterceptor()
    monkeypatch.setattr("builtins.open", simula_erro)

    entrada = "<writefile path=\"qualquer.txt\">conteúdo</writefile>"
    saida = interceptor.process(entrada)

    # erro deve ter sido logado, mas texto continua limpo
    assert not "<writefile" in saida
