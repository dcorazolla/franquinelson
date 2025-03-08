import os
import json
from .config import ESTADO_FILE
from .debug import log_debug

def salvar_estado(contexto):
    estado = {"contexto": contexto}
    try:
        with open(ESTADO_FILE, "w", encoding="utf-8") as f:
            json.dump(estado, f)
        log_debug(f"Estado salvo em {ESTADO_FILE}")
    except Exception as e:
        log_debug(f"Erro ao salvar estado: {str(e)}")

def carregar_estado():
    if os.path.exists(ESTADO_FILE):
        try:
            with open(ESTADO_FILE, "r", encoding="utf-8") as f:
                estado = json.load(f)
            log_debug(f"Estado carregado de {ESTADO_FILE}")
            print(f"Carregando estado anterior")
            return estado.get("contexto", None)
        except Exception as e:
            log_debug(f"Erro ao carregar estado: {str(e)}")
    return None
