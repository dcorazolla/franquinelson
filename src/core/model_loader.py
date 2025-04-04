# src/core/model_loader.py
import os
import requests
from tqdm import tqdm
from config.settings import config
from src.core.util.logger import Logger
from llama_cpp import Llama

class ModelLoader:
    """
    Classe responsável pelo carregamento automático do modelo de linguagem.

    Gerencia o download seguro e transparente do modelo, exibe o progresso,
    verifica existência prévia e carrega o modelo na memória para uso.
    """

    def __init__(self):
        """
        Inicializa o ModelLoader com configurações básicas e logger.
        """
        self.logger = Logger()
        self.model_name = config.MODEL_NAME
        self.model_dir = config.MODEL_DIR
        self.model_file = os.path.join(self.model_dir, config.MODEL_FILE)
        self.model_url = config.MODEL_URL
        self.verbose = config.VERBOSE

    def _model_exists(self) -> bool:
        """
        Verifica se o modelo já está presente no diretório especificado.

        Returns:
            bool: True se o arquivo do modelo existir, False caso contrário.
        """
        self.logger.debug("Verificando se modelo está disponível")
        return os.path.exists(self.model_file)

    def download_model(self):
        """
        Baixa o modelo do servidor configurado exibindo uma barra de progresso.

        Não realiza download se o modelo já existir localmente.
        """
        if self._model_exists():
            self.logger.debug("Modelo já existe [%s]. Pulando download.", self.model_file)
            return

        self.logger.debug("Baixando modelo %s de %s...", self.model_name, self.model_url)

        os.makedirs(self.model_dir, exist_ok=True)

        response = requests.get(self.model_url, stream=True, timeout=60, verify=False)
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
        """
        Carrega o modelo na memória, realizando o download caso necessário.

        Returns:
            Llama: Instância do modelo carregado pronto para execução.
        """
        if not self._model_exists():
            self.download_model()

        self.logger.info("Carregando modelo...")

        model = Llama(
            model_path=self.model_file,
            temperature=config.TEMPERATURE,
            verbose=config.VERBOSE,
            n_ctx=config.CONTEXT_SIZE
        )

        self.logger.info("Modelo carregado com sucesso!")
        return model
