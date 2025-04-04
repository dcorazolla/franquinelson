#src/main.py
from .core.assistant import Assistant

def main():
    """ Função principal que inicializa o assistente. """

    assistant = Assistant()
    assistant.chat()

if __name__ == "__main__":
    main()