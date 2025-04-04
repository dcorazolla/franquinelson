# src/core/interceptors/output_interceptor.py
from .base import BaseInterceptor

class OutputInterceptor(BaseInterceptor):
    """
    Classe base para interceptadores de saída.

    Interceptadores derivados desta classe atuam sobre o output (saída)
    gerado pelo assistente antes de ser exibido ao usuário.
    """
    pass
