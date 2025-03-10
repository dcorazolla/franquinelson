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
        "file": "bode-7b-alpaca-q4_k_m.gguf",
        "url": "https://huggingface.co/recogna-nlp/bode-7b-alpaca-pt-br-gguf/resolve/main/bode-7b-alpaca-q4_k_m.gguf?download=true",
        "n_ctx": 1024,
        "n_threads": 4,
        "temperature": 0.3,
        "verbose": False,
        "max_tokens": 600
    }
}
