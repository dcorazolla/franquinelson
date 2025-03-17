from .assistant import FranquinelsonAssistant

def main():
    """ Função principal que inicializa o assistente. """

    assistant = FranquinelsonAssistant()
    assistant.chat()

if __name__ == "__main__":
    main()