import os
import json
from .config import CONFIG
from .debug import log_debug

def state_save(contexto):
    estado = {"contexto": contexto}
    try:
        with open(CONFIG["state"]["file"], "w", encoding="utf-8") as f:
            json.dump(estado, f)
        log_debug(f"Estado salvo em {CONFIG['state']['file']}")
    except Exception as e:
        log_debug(f"Erro ao salvar estado: {str(e)}")

def state_load():
    if os.path.exists(CONFIG["state"]["file"]):
        try:
            with open(CONFIG["state"]["file"], "r", encoding="utf-8") as f:
                estado = json.load(f)
            log_debug(f"Estado carregado de {CONFIG['state']['file']}")
            print(f"Carregando estado anterior")
            return estado.get("contexto", None)
        except Exception as e:
            log_debug(f"Erro ao carregar estado: {str(e)}")
    return None
