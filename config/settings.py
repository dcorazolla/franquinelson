import os

class Config:
    """
    Classe de configuração centralizada para o assistente Franquinelson.
    """

    # -------------------------------
    # 🏗️ Configuração de Diretórios
    # -------------------------------
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR: str = os.path.join(BASE_DIR, "models")
    PERSONALITY_FILE: str = os.path.join(BASE_DIR, "config", "personality.txt")

    # -------------------------------
    # 🤖 Configuração do Modelo
    # -------------------------------
    MODEL_NAME: str = "recogna-nlp/bode-7b-alpaca-pt-br-gguf"  # Modelo Bode em português do Brasil
    MODEL_FILE: str = "bode-7b-alpaca-q4_k_m.gguf"  # Nome do arquivo do modelo GGUF
    MODEL_URL: str = f"https://huggingface.co/{MODEL_NAME}/resolve/main/{MODEL_FILE}"
    AUTO_DOWNLOAD: bool = True  # Baixar modelo automaticamente se não existir
    DOWNLOAD_TIMEOUT: int = 600  # Tempo limite para download em segundos

    # -------------------------------
    # ⚙️ Configuração de Execução
    # -------------------------------
    USE_CPU: bool = True  # Troque para False se quiser rodar em GPU
    DEVICE: str = "cpu" if USE_CPU else "cuda"
    CONTEXT_SIZE: int = 2048  # Quantidade de tokens de contexto armazenados

    # -------------------------------
    # 🎭 Configuração do Assistente
    # -------------------------------
    ASSISTANT_NAME: str = "Franquinelson"  # Nome do assistente
    TEMPERATURE: float = 0.3  # Controla a criatividade das respostas (0.1 = previsível, 1.0 = criativo)

    # -------------------------------
    # 🛠️ Configuração de Depuração
    # -------------------------------
    DEBUG: bool = False  # Ativar ou desativar logs detalhados
    VERBOSE: bool = False  # Ativar ou desativar respostas detalhadas

    @classmethod
    def to_dict(cls) -> dict:
        """ Retorna as configurações como um dicionário. """
        return {key: value for key, value in cls.__dict__.items() if not key.startswith("__")}

# Instância única da configuração
config = Config()
