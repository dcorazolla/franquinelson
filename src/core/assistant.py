from config.settings import config
from .prompt_builder import PromptBuilder
from src.core.util.logger import Logger
from src.core.model_loader import ModelLoader


class FranquinelsonAssistant:

    def __init__(self):
        self.logger = Logger()

        self.logger.debug("Iniciando assistente")

        self.prompt_builder = PromptBuilder()
        self.model = ModelLoader().load_model()
        self.chat_history = []

    def chat(self):
        print(f"{config.ASSISTANT_NAME} está online. Digite 'sair' para sair.")

        while True:
            user_input = input("\nVocê: ").strip()

            if user_input.lower() in ['exit', 'quit', 'sair', 'bye']:
                print("Até logo! 😊")
                break

            try:
                resposta = self.response(user_input)
                print(f"\n{config.ASSISTANT_NAME}: {resposta}")
            
            except ValueError as exception:
                print(f"\n{config.ASSISTANT_NAME}: Desculpe, tive um erro ao processar a questão.")
                
                if "exceed context window" in str(exception):
                    print(f"\n{config.ASSISTANT_NAME}: Limpando o histórico...")
                    self.history = []
                    print(f"\n{config.ASSISTANT_NAME}: Poderia repetir?")
                else:
                    raise exception
                
    def response(self, user_input: str) -> str:
        prompt = self.prompt_builder.generate_prompt(user_input, self.chat_history)
        self.logger.debug("Enviando prompt...")
        response = self.model(
            prompt, 
            max_tokens=config.MAX_TOKENS, 
            temperature=config.TEMPERATURE
        )
        cleaned_response = self.prompt_builder.clean_response(response['choices'][0]['text'])
        self.chat_history.append({"pergunta": user_input, "resposta": cleaned_response})
        return cleaned_response