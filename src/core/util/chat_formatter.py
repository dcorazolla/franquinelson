# src/core/util/chat_formatter.py
class ChatFormatter:
    @staticmethod
    def format_instruction_prompt(system_message, history, user_input):
        """
        Formata o prompt no estilo Alpaca Instruct, incluindo histórico e a nova pergunta.
        """
        history_lines = []
        for item in history:
            question = item.get("pergunta", "").strip()
            answer = item.get("resposta", "").strip()
            history_lines.append(f"Usuário: {question}\nAssistente: {answer}")

        history_text = "\n".join(history_lines)

        prompt = f"### Sistema:\n{system_message}\n\n"
        if history_lines:
            prompt += f"### Conversa:\n{history_text}\n\n"
        prompt += f"### Instrução:\n{user_input.strip()}\n\n"
        prompt += "### Resposta:\n"

        return prompt
