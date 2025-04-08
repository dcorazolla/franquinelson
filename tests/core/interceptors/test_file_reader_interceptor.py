import pytest
from src.core.interceptors.implementations.file_reader import FileReaderInterceptor

def test_readfile_existente(tmp_path):
    test_file = tmp_path / "exemplo.txt"
    test_file.write_text("conteúdo de exemplo", encoding="utf-8")

    entrada = f"<readfile path=\"{test_file}\" />"
    interceptor = FileReaderInterceptor()
    saida = interceptor.process(f"Ler: {entrada}")

    assert "[INÍCIO DO ARQUIVO:" in saida
    assert "conteúdo de exemplo" in saida
    assert "[FIM DO ARQUIVO]" in saida

def test_readfile_inexistente():
    entrada = "<readfile path=\"nao_existe.txt\" />"
    interceptor = FileReaderInterceptor()
    saida = interceptor.process(entrada)

    assert "[Erro: Arquivo 'nao_existe.txt' não encontrado.]" in saida
