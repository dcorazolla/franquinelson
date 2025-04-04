# src/core/interceptors/input_interceptor.py
from .base import BaseInterceptor

class InputInterceptor(BaseInterceptor):
    """
    Classe base para interceptadores de entrada.

    Interceptadores derivados desta classe atuam sobre o input (entrada)
    fornecido pelo usuário antes de ser enviado ao assistente.
    """
    pass
