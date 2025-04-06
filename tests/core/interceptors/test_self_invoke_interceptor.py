import pytest
from src.core.interceptors.implementations.self_invoke import SelfInvokeInterceptor

def test_self_invoke_simples():
    interceptor = SelfInvokeInterceptor()
    texto = "<rerun>Nova instrução simples</rerun>"
    
    resultado = interceptor.process(texto)
    
    assert resultado == "Nova instrução simples"

def test_self_invoke_limite_rerun():
    interceptor = SelfInvokeInterceptor()
    texto = "<rerun>Executar novamente</rerun>"
    
    # Executar o rerun até o limite
    for _ in range(SelfInvokeInterceptor.MAX_RERUNS):
        resultado = interceptor.process(texto)
        assert resultado == "Executar novamente"

    # Após atingir o limite, deve parar de executar
    resultado_excedido = interceptor.process(texto)
    assert resultado_excedido == ""
