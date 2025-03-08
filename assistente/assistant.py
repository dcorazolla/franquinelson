from llama_cpp import Llama
from .config import MODEL_PATH, N_CTX, N_THREADS
from .prompt import criar_prompt, limpar_resposta
from .state import carregar_estado, salvar_estado
from .project_executor import executar_projeto, processar_resposta
from .commands import executar_comando_seguro
from .debug import log_debug

def chat():
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        verbose=False
    )
    print("🖥️ Assistente com Debug, Memória Persistente e Execução de Projetos")
    print("Digite 'sair' para encerrar ou inicie um projeto com 'Projeto: [descrição]'")
    contexto_comando = carregar_estado() or None
    if contexto_comando:
        print("[INFO] Contexto persistente carregado.")
    
    while True:
        try:
            user_input = input("Você: ").strip()
            if user_input.lower() in ["sair", "xau"]:
                print("Assistente: Até mais! 🚀")
                salvar_estado(contexto_comando)
                break
            if user_input.lower().startswith("projeto:"):
                projeto = user_input[len("projeto:"):].strip()
                executar_projeto(projeto, llm)  # Passa o llm como argumento
                continue
            if user_input.startswith("Execute comando:"):
                comando = user_input.split(":", 1)[1].strip()
                resultado, _ = executar_comando_seguro(comando)
                print(f"\n🔧 Resultado:\n{resultado}\n")
                continue
            prompt = criar_prompt(user_input, contexto_comando)
            response = llm(prompt, max_tokens=250, temperature=0.6)
            resposta_bruta = response['choices'][0]['text']
            log_debug(f"Resposta bruta: {resposta_bruta}")
            resposta = limpar_resposta(resposta_bruta)
            if "{{comando:" in resposta or "{{arquivo:" in resposta:
                resposta = processar_resposta(resposta)
                contexto_comando = resposta
            else:
                contexto_comando = None
            print(f"Assistente: {resposta}")
            salvar_estado(contexto_comando)
        except Exception as e:
            log_debug(f"Erro: {str(e)}")
            print(f"Erro: {str(e)}")
