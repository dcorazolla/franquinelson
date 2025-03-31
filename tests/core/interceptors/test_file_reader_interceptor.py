import os
import pytest
from src.core.interceptors.file_reader_interceptor import FileReaderInterceptor

@pytest.fixture
def interceptor():
    return FileReaderInterceptor()

def test_readfile_success(tmp_path, interceptor):
    file = tmp_path / "test.txt"
    file.write_text("Conteúdo de teste.")
    prompt = f"Leia isto: ##readfile: {file}## e comente."
    output = interceptor.process(prompt)
    assert "Conteúdo de teste." in output

def test_readfile_not_found(interceptor):
    prompt = "##readfile: inexistente.txt##"
    output = interceptor.process(prompt)
    assert "[Erro: Arquivo" in output

def test_readfile_invalid(interceptor, monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *_: (_ for _ in ()).throw(IOError("falha")))
    prompt = "##readfile: qualquer.txt##"
    output = interceptor.process(prompt)
    assert "[Erro ao ler o arquivo" in output
