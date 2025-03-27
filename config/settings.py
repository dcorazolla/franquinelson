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
    MODEL_NAME: str = "recogna-nlp/bode-7b-alpaca-pt-br-gguf"
    MODEL_FILE: str = "bode-7b-alpaca-q4_k_m.gguf"
    AUTO_DOWNLOAD: bool = True
    MODEL_URL: str = f"https://huggingface.co/recogna-nlp/bode-7b-alpaca-pt-br-gguf/resolve/main/{MODEL_FILE}"

    # -------------------------------
    # Configuração do Comportamento
    # -------------------------------
    TEMPERATURE: float = 0.5
    LOG_LEVEL: int = DEBUG
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
    CONTEXT_SIZE: int = 2048
    if DEVICE == "cpu":
        N_THREADS: int = 4
    elif DEVICE == "cuda":
        N_THREADS: int = torch.cuda.device_count() * 2
    else:
        N_THREADS: int = 2
    MAX_TOKENS: int = 600

    # -------------------------------
    # Configuração do Assistente
    # -------------------------------
    ASSISTANT_NAME: str = "Franquinelson"

    @classmethod
    def to_dict(cls) -> dict:
        """ Retorna as configurações como um dicionário. """
        return {key: value for key, value in cls.__dict__.items() if not key.startswith("__")}

# Instância única da configuração
config = Config()
