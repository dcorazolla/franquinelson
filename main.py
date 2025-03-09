from assistente.assistant import chat
from assistente.model import verify

if __name__ == "__main__":
    print("\nVerificando modelo")
    if verify():
        print("\nAssistente iniciado.")
        chat()
