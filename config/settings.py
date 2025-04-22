import os
import torch
from logging import DEBUG,INFO

class Config:
    """
    Classe de configuração centralizada para o assistente.
    """

    # -------------------------------
    # Configuração de Diretórios
    # -------------------------------
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR: str = os.path.join(BASE_DIR, "models")

    # -------------------------------
    # Configuração do Modelo
    # -------------------------------
    MODEL_NAME: str = "TheBloke/deepseek-llm-7B-chat-GGUF"
    MODEL_FILE: str = "deepseek-llm-7b-chat.Q4_K_M.gguf"
    AUTO_DOWNLOAD: bool = True
    MODEL_URL: str = f"https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF/resolve/main/{MODEL_FILE}"

    # -------------------------------
    # Configuração do Comportamento
    # -------------------------------
    TEMPERATURE: float = 0.6
    LOG_LEVEL: int = INFO
    VERBOSE: bool = False
    PERSONALITY_FILE: str = "config/personality.txt"

    # -------------------------------
    # Configuração de Execução
    # -------------------------------
    print("Detectando device para execução do modelo.")
    if torch.backends.mps.is_available():
        DEVICE: str = "mps"  # Para Macs com Apple Silicon (M1/M2)
    elif torch.cuda.is_available():
        DEVICE: str = "cuda"  # Para GPUs NVIDIA
    else:
        try:
            if torch.backends.hip.is_available():  # Apenas se a versão do torch suportar
                DEVICE = "hip"  # Para GPUs AMD (ROCm)
            else:
                DEVICE = "cpu"
        except AttributeError:
            DEVICE = "cpu"
    print(f"Dispositivo detectado: {DEVICE}")

    CONTEXT_SIZE: int = 8192
    if DEVICE == "cpu":
        N_THREADS: int = 4
    elif DEVICE == "cuda":
        N_THREADS: int = torch.cuda.device_count() * 2
    else:
        N_THREADS: int = 4
    MAX_TOKENS: int = 1024

    # -------------------------------
    # Configuração do Assistente
    # -------------------------------
    ASSISTANT_NAME: str = "Franquinelson"
    ENABLE_SPEECH: bool = True

    @classmethod
    def to_dict(cls) -> dict:
        """ Retorna as configurações como um dicionário. """
        return {key: value for key, value in cls.__dict__.items() if not key.startswith("__")}

# Instância única da configuração
config = Config()
