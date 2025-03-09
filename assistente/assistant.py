from llama_cpp import Llama
from .config import CONFIG
from .prompt import criar_prompt, limpar_resposta
from .state import state_load, state_save
from .project_executor import executar_projeto, processar_resposta
from .commands import executar_comando_seguro
from .debug import log_debug

def chat():

    llm = Llama(
        model_path=CONFIG["model"]["path"] + CONFIG["model"]["file"],
        n_ctx=CONFIG["model"]["n_ctx"],
        n_threads=CONFIG["model"]["n_threads"],
        verbose=CONFIG["model"]["verbose"],
        temperature=CONFIG["model"]["temperature"]
    )

    print("🖥️ Assistente virtual")
    print("Digite 'sair' para encerrar'")

    contexto_comando = state_load() or None
    if contexto_comando:
        print("[INFO] Contexto persistente carregado.")
    
    while True:
        try:
            user_input = input("Você: ").strip()
            if user_input.lower() in ["sair", "xau", "bye", "fui"]:
                print(f"Assistente: Até mais!")
                state_save(contexto_comando)
                break
    #         if user_input.lower().startswith("projeto:"):
    #             projeto = user_input[len("projeto:"):].strip()
    #             executar_projeto(projeto, llm)
    #             continue
            if user_input.startswith("comando:"):
                comando = user_input.split(":", 1)[1].strip()
                resultado, _ = executar_comando_seguro(comando)
                print(f"\n🔧 Resultado:\n{resultado}\n")
                continue
            prompt = criar_prompt(user_input, contexto_comando)
            response = llm(prompt, max_tokens=CONFIG["model"]["max_tokens"], temperature=CONFIG["model"]["temperature"])
            resposta_bruta = response['choices'][0]['text']
            log_debug(f"Resposta bruta: {resposta_bruta}")
            resposta = limpar_resposta(resposta_bruta)
    #         if "{{comando:" in resposta or "{{arquivo:" in resposta:
    #             resposta = processar_resposta(resposta)
    #             contexto_comando = resposta
    #         else:
    #             contexto_comando = None
            print(f"Assistente: {resposta}")
            state_save(contexto_comando)
        except Exception as e:
            log_debug(f"Erro: {str(e)}")
            print(f"Erro: {str(e)}")
