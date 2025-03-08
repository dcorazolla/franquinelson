import re
from .prompt import limpar_resposta
from .file_manager import criar_arquivo
from .commands import executar_comando_seguro
from .debug import log_debug

def dividir_tarefas(projeto, llm) -> list:
    prompt_dividir = f"Divida a seguinte tarefa em uma lista de subtarefas numeradas, uma por linha, sem explicações extras: '{projeto}'"
    log_debug(f"Prompt para dividir tarefas: {prompt_dividir}")
    response = llm(prompt_dividir, max_tokens=150, temperature=0.5)
    tarefas_bruto = response['choices'][0]['text']
    tarefas_limpo = limpar_resposta(tarefas_bruto)
    log_debug(f"Tarefas geradas:\n{tarefas_limpo}")
    tarefas = [t.strip() for t in tarefas_limpo.split('\n') if t.strip()]
    return tarefas

def executar_tarefa(tarefa, llm) -> str:
    prompt_tarefa = f"Execute a seguinte tarefa de forma detalhada, dividindo-a se necessário e gerando os arquivos correspondentes usando '{{arquivo: nome_do_arquivo}}'. Tarefa: {tarefa}"
    log_debug(f"Prompt para tarefa: {prompt_tarefa}")
    response = llm(prompt_tarefa, max_tokens=300, temperature=0.6)
    resposta_bruta = response['choices'][0]['text']
    resposta = limpar_resposta(resposta_bruta)
    resposta = processar_resposta(resposta)
    return resposta

def processar_resposta(resposta: str) -> str:
    # Processa execução de comandos
    marcador_cmd = re.search(r'\{\{comando:\s*(.*?)\}\}', resposta)
    if marcador_cmd:
        comando = marcador_cmd.group(1).strip()
        from .commands import COMANDOS_PERMITIDOS, executar_comando_seguro  # Import local para evitar circularidade
        if comando in COMANDOS_PERMITIDOS:
            resultado, _ = executar_comando_seguro(comando)
            resposta = resposta.replace(marcador_cmd.group(0), resultado.strip())
        else:
            resposta = resposta.replace(marcador_cmd.group(0), "[Comando não permitido]")
    # Processa criação de arquivos
    marcador_arquivo = re.search(r'\{\{arquivo:\s*(.*?)\}\}', resposta)
    if marcador_arquivo:
        nome_arquivo = marcador_arquivo.group(1).strip()
        conteudo = resposta.split(marcador_arquivo.group(0))[-1].strip()
        resultado_arquivo = criar_arquivo(nome_arquivo, conteudo, pasta="projetos")
        resposta = resposta.replace(marcador_arquivo.group(0), resultado_arquivo)
    return resposta

def executar_projeto(projeto, llm):
    print(f"\nIniciando projeto: {projeto}")
    tarefas = dividir_tarefas(projeto, llm)
    if not tarefas:
        print("Nenhuma tarefa foi gerada.")
        return
    print("\nLista de tarefas geradas:")
    for i, tarefa in enumerate(tarefas, start=1):
        print(f"{i}. {tarefa}")
    for i, tarefa in enumerate(tarefas, start=1):
        print(f"\nExecutando tarefa {i}: {tarefa}")
        resultado_tarefa = executar_tarefa(tarefa, llm)
        print(f"Resultado da tarefa {i}: {resultado_tarefa}")
    print("\nProjeto concluído.")
