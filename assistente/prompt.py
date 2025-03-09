import re
from .debug import log_debug

def criar_prompt(pergunta, contexto_comando=None):
    contexto_str = f"\nResultado do comando anterior: {contexto_comando}\n" if contexto_comando else ""
    prompt = f"""### INSTRUÇÕES:
Você se chama Franquinelson, é um assistente brasileiro especializado em tecnologia, que responde em português de forma curta e objetiva e usa alguns emoticons.
- Se necessário, utilize 'comando: nome_do_comando' para executar comandos.
- Se precisar criar arquivos, utilize 'arquivo: nome_do_arquivo' e coloque o conteúdo após o marcador.
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
