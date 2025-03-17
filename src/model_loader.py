import os
import requests
from tqdm import tqdm
from config.settings import config
from src.util.logger import Logger
from llama_cpp import Llama

class ModelLoader:
    """
    Classe responsável pelo carregamento do modelo de IA.
    """

    def __init__(self):
        self.logger = Logger()
        self.model_name = config.MODEL_NAME
        self.model_dir = config.MODEL_DIR
        self.model_file = os.path.join(self.model_dir, config.MODEL_FILE)
        self.model_url = config.MODEL_URL
        self.verbose = config.VERBOSE

    def _model_exists(self) -> bool:
        """ Verifica se o modelo já foi baixado. """
        self.logger.debug("Verificando se modelo está disponível")
        return os.path.exists(self.model_file)

    def download_model(self):
        """ Faz o download do modelo com barra de progresso. """
        if self._model_exists():
            self.logger.debug("Modelo já existe [%s]. Pulando download.", self.model_file)
            return

        self.logger.debug("Baixando modelo %s de %s...", self.model_name, self.model_url)

        os.makedirs(self.model_dir, exist_ok=True)

        response = requests.get(self.model_url, stream=True, timeout=60)
        if response.status_code != 200:
            raise RuntimeError(f"Erro ao baixar o modelo. Código HTTP: {response.status_code}")

        total_size = int(response.headers.get("content-length", 0))

        with open(self.model_file, "wb") as file, tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Baixando modelo", disable=not self.verbose
        ) as progress:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    progress.update(len(chunk))

        self.logger.debug("Download concluído!")

    def load_model(self):
        """ Carrega o modelo GGUF na memória, baixando se necessário. """
        if not self._model_exists():
            self.download_model()

        self.logger.info("Carregando modelo...")

        model = Llama(
            model_path=self.model_file,
            temperature=config.TEMPERATURE,
            verbose=config.VERBOSE
        )

        self.logger.info("Modelo carregado com sucesso!")
        return model
