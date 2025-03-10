from colorama import init
from src.assistant import FranquinelsonAssistant

def main():
    init(autoreset=True)

    assistant = FranquinelsonAssistant()
    assistant.chat()

if __name__ == "__main__":
    main()
