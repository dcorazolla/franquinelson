from .config import CONFIG

def log_debug(msg: str):
    if CONFIG["debug"]:
        print(f"[DEBUG] {msg}")
