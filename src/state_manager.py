import json
import os
from .utils.logger import log_debug
from tqdm import tqdm


class StateManager:
    def __init__(self, state_file, debug=False):
        self.state_file = state_file
        self.debug = debug

    def save_state(self, context):
        try:
            with tqdm(total=1, desc="Salvando estado", unit="estado") as progress_bar:
                with open(self.state_file, 'w', encoding='utf-8') as file:
                    json.dump({"context": context}, file, ensure_ascii=False, indent=4)
                progress_bar.update(1)
            log_debug(f"Estado salvo com sucesso em {self.state_file}", self.debug)
        except (IOError, OSError) as error:
            log_debug(f"Erro ao salvar estado: {error}", self.debug)

    def load_state(self):
        if not os.path.exists(self.state_file):
            log_debug(f"Arquivo de estado não encontrado: {self.state_file}", self.debug)
            return None

        try:
            with tqdm(total=1, desc="Carregando estado", unit="estado") as progress_bar:
                with open(self.state_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    progress_bar.update(1)
            log_debug("Estado carregado com sucesso.", self.debug)
            return data.get('context', None)
        except (IOError, json.JSONDecodeError, OSError) as error:
            log_debug(f"Erro ao carregar estado: {error}", self.debug)
            return None
