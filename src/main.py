from src.chatbot import chatbot

def main():
    """ Inicia a interação com o assistente via terminal. """
    print("Assistente iniciado! Digite 'sair' para encerrar.")

    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Encerrando o assistente. Até mais!")
            break
        
        response = chatbot.generate_response(user_input)
        print(f"Assistente: {response}")

if __name__ == "__main__":
    main()
