from src.core.interceptors.implementations.self_invoke import SelfInvokeInterceptor

def test_rerun_uma_instrucao():
    interceptor = SelfInvokeInterceptor()
    entrada = "<rerun>Nova pergunta</rerun>"

    saida = interceptor.process(entrada)

    assert saida == "Nova pergunta"

def test_rerun_limite_execucoes():
    interceptor = SelfInvokeInterceptor()
    entrada = "<rerun>Loop infinito</rerun>"

    # até o limite
    for _ in range(interceptor.MAX_RERUNS):
        saida = interceptor.process(entrada)
        assert saida == "Loop infinito"

    # após o limite
    saida = interceptor.process(entrada)
    assert saida == ""
