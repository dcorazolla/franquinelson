import os

CONFIG = {
    "debug": True,
    "name": "Franquinelson",
    "state": {
        "enabled": True,
        "file": "./state.json"
    },
    "model": {
        "path": os.path.expanduser("./models/"),
        "file": "llama-2-7b-chat.Q4_K_M.gguf",
        "url": "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf?download=true",
        "n_ctx": 768,
        "n_threads": 4,
        "temperature": 0.3,
        "verbose": False,
        "max_tokens": 600
    }
}
