from src.model_loader import model_loader
from config.settings import config

class Chatbot:
    """
    Classe principal para gerenciar as interações do assistente de IA.
    - Mantém um contexto curto da conversa.
    - Gera respostas baseadas na entrada do usuário.
    - Garante que as respostas sejam sempre em português do Brasil.
    - Usa um arquivo externo para carregar a personalidade do assistente.
    """

    def __init__(self, context_size=5):
        self.model = model_loader.load_model()
        self.context_size = context_size  # Número de interações anteriores a serem mantidas
        self.history = []  # Histórico da conversa
        self.verbose = config.VERBOSE
        self.debug = config.DEBUG
        self.assistant_name = config.ASSISTANT_NAME
        self.personality = self._load_personality()

    def _log(self, message):
        """Exibe logs apenas se VERBOSE ou DEBUG estiver ativado."""
        if self.verbose or self.debug:
            print(message)

    def _load_personality(self):
        """Carrega a personalidade do assistente a partir do arquivo."""
        try:
            with open(config.PERSONALITY_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"{self.assistant_name} é um assistente de IA especializado em TI, fornecendo respostas diretas e técnicas."

    def generate_response(self, user_input):
        """ Gera uma resposta para a entrada do usuário garantindo que seja em português. """
        self.history.append(f"Usuário: {user_input}")
        conversation = f"{self.personality}\n\n" + "\n".join(self.history)

        self._log(f"Enviando entrada ao modelo:\n{conversation}")

        response = self.model(
            conversation,
            max_tokens=200,
            stop=["Usuário:", f"{self.assistant_name}:"],  # Evita que o modelo continue indefinidamente
            echo=False,
            temperature=config.TEMPERATURE  # Aplica temperatura configurada
        )["choices"][0]["text"].strip()

        # Garante que a resposta esteja em português
        if not response.strip():
            response = "Desculpe, não entendi. Pode reformular a pergunta?"

        self.history.append(f"{self.assistant_name}: {response}")

        # Mantém um histórico curto
        if len(self.history) > self.context_size * 2:
            self.history = self.history[-(self.context_size * 2):]

        self._log(f"Resposta gerada:\n{response}")
        return response

# Instância global do chatbot
chatbot = Chatbot()
