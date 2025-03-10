from datetime import datetime
from config import CONFIG

def log_debug(message, debug=True):
    if CONFIG.get("debug", False) and debug:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[DEBUG {current_time}] {message}")
