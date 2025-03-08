from .config import DEBUG

def log_debug(msg: str):
    if DEBUG:
        print(f"[DEBUG] {msg}")
