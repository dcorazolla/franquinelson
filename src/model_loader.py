import os
import requests
from tqdm import tqdm
from config.settings import config
from llama_cpp import Llama

class ModelLoader:
    """
    Classe responsável pelo carregamento do modelo de IA.
    - Baixa automaticamente se não existir.
    - Exibe progresso do download no terminal.
    - Carrega modelos no formato GGUF usando llama-cpp-python.
    - Respeita configurações de depuração e logs.
    """

    def __init__(self):
        self.model_name = config.MODEL_NAME
        self.model_dir = config.MODEL_DIR
        self.model_file = os.path.join(self.model_dir, config.MODEL_FILE)
        self.model_url = config.MODEL_URL
        self.verbose = config.VERBOSE
        self.debug = config.DEBUG

    def _log(self, message):
        """Exibe logs apenas se VERBOSE ou DEBUG estiver ativado."""
        if self.verbose or self.debug:
            print(message)

    def _model_exists(self) -> bool:
        """ Verifica se o modelo já foi baixado. """
        return os.path.exists(self.model_file)

    def download_model(self):
        """ Faz o download do modelo com barra de progresso. """
        if self._model_exists():
            self._log(f"Modelo já existe em {self.model_file}. Pulando download.")
            return

        self._log(f"Baixando modelo {self.model_name} de {self.model_url}...")

        os.makedirs(self.model_dir, exist_ok=True)

        response = requests.get(self.model_url, stream=True, timeout=config.DOWNLOAD_TIMEOUT)
        if response.status_code != 200:
            raise RuntimeError(f"Erro ao baixar o modelo. Código HTTP: {response.status_code}")

        total_size = int(response.headers.get("content-length", 0))

        with open(self.model_file, "wb") as file, tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Baixando modelo"
        ) as progress:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    progress.update(len(chunk))

        self._log("Download concluído!")

    def load_model(self):
        """ Carrega o modelo GGUF na memória, baixando se necessário. """
        if not self._model_exists():
            self.download_model()

        self._log(f"Carregando modelo {self.model_name}...")

        model = Llama(
            model_path=self.model_file,
            temperature=config.TEMPERATURE,  # Usa a temperatura configurada
        )

        self._log("Modelo carregado com sucesso!")
        return model

# Instância global do loader
model_loader = ModelLoader()
