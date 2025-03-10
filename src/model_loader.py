import os
import requests
from tqdm import tqdm
import llama_cpp
from config import CONFIG
from .utils.logger import log_debug


class ModelLoader:
    def __init__(self, debug=False):
        self.model_path = f"{CONFIG['model']['path']}{CONFIG['model']['file']}"
        self.model_url = CONFIG["model"]["url"]
        self.n_ctx = CONFIG["model"]["n_ctx"]
        self.n_threads = CONFIG["model"]["n_threads"]
        self.verbose = CONFIG["model"]["verbose"]
        self.debug = debug

    def model_exists(self):
        exists = os.path.isfile(self.model_path)
        log_debug(f"Modelo existe: {'Sim' if exists else 'Não'}", self.debug)
        return exists

    def download_model(self):
        os.makedirs(CONFIG['model']['path'], exist_ok=True)
        response = requests.get(CONFIG['model']['url'], stream=True, timeout=300)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(self.model_path, 'wb') as file, tqdm(
            desc="Baixando Modelo",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        
        log_debug("Modelo baixado com sucesso.", self.debug)

    def load_model(self):
        if not self.model_exists():
            self.download_model()

        log_debug("Iniciando carga do modelo...", self.debug)

        model = llama_cpp.Llama(
            model_path=self.model_path,
            n_ctx=CONFIG["model"]["n_ctx"],
            n_threads=CONFIG["model"]["n_threads"],
            verbose=CONFIG["model"]["verbose"]
        )

        log_debug("Modelo carregado com sucesso.", self.debug)
        return model
