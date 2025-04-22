# src/core/util/chat_formatter.py
class ChatFormatter:
    """
    Classe utilitária para formatação consistente de prompts de interação com o modelo,
    utilizando o padrão Alpaca Instruct.

    Formata o prompt incluindo mensagem de sistema, histórico de conversa anterior e instrução atual.
    """

    @staticmethod
    def format_instruction_prompt(system_message, history, user_input):
        """
        Formata o prompt final no padrão ChatML (<|user|>, <|assistant|>), usado pelo DeepSeek.

        Args:
            system_message (str): Mensagem inicial que define o contexto ou personalidade.
            history (list): Histórico da conversa com perguntas e respostas anteriores.
            user_input (str): Instrução ou pergunta atual feita pelo usuário.

        Returns:
            str: Prompt formatado completo.
        """
        prompt = f"<|system|>\n{system_message.strip()}\n"
        
        for item in history:
            pergunta = item.get("pergunta", "").strip()
            resposta = item.get("resposta", "").strip()
            prompt += f"<|user|>\n{pergunta}\n<|assistant|>\n{resposta}\n"

        prompt += f"<|user|>\n{user_input.strip()}\n<|assistant|>\n"

        return prompt

    # @staticmethod
    # def format_instruction_prompt(system_message, history, user_input):
    #     """
    #     Formata o prompt final que será enviado ao modelo.

    #     Args:
    #         system_message (str): Mensagem inicial que define o contexto ou personalidade.
    #         history (list): Histórico da conversa com perguntas e respostas anteriores.
    #         user_input (str): Instrução ou pergunta atual feita pelo usuário.

    #     Returns:
    #         str: Prompt formatado completo.
    #     """
    #     history_lines = []
    #     for item in history:
    #         question = item.get("pergunta", "").strip()
    #         answer = item.get("resposta", "").strip()
    #         history_lines.append(f"Usuário: {question}\nAssistente: {answer}")

    #     history_text = "\n".join(history_lines)

    #     prompt = f"### Sistema:\n{system_message}\n\n"
    #     if history_lines:
    #         prompt += f"### Conversa:\n{history_text}\n\n"
    #     prompt += f"### Instrução:\n{user_input.strip()}\n\n"
    #     prompt += "### Resposta:\n"

    #     return prompt
