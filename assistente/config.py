import os

# Configurações gerais
DEBUG = False
ESTADO_FILE = os.path.expanduser("/app/assistente/assistente_estado.json")
MODEL_PATH = os.path.expanduser("/app/models/llama-2-7b-chat.Q4_K_M.gguf")

# Parâmetros do modelo
N_CTX = 1024
N_THREADS = 6
