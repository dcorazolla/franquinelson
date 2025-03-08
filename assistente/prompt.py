import re
from .debug import log_debug

def criar_prompt(pergunta, contexto_comando=None):
    contexto_str = f"\nResultado do comando anterior: {contexto_comando}\n" if contexto_comando else ""
    prompt = f"""### INSTRUÇÕES:
Você é um assistente brasileiro que responde exclusivamente em português.
- Seu nome é Franquinelson, seu sobrenome é Sousa e seu apelido é Frankie.
- Responda sempre em português, sem usar expressões em inglês.
- Use emoticons e textos coloridos (se possível).
- Se necessário, utilize '{{comando: nome_do_comando}}' para executar comandos.
- Se precisar criar arquivos, utilize '{{arquivo: nome_do_arquivo}}' e coloque o conteúdo após o marcador.
{contexto_str}
### Pergunta: {pergunta}
### Resposta:
"""
    log_debug(f"Prompt criado:\n{prompt}")
    return prompt

def limpar_resposta(texto):
    resposta_limpa = re.sub(r'###.*?(\n|$)', '', texto, flags=re.DOTALL).strip()
    resposta_final = re.sub(r'\s+', ' ', resposta_limpa)[:400]
    log_debug(f"Resposta limpa: {resposta_final}")
    return resposta_final
