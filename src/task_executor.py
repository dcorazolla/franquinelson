import os
import re
from tqdm import tqdm
from config import CONFIG
from .utils.logger import log_debug

class TaskExecutor:
    def __init__(self, assistant, debug=False):
        self.assistant = assistant
        self.debug = debug

    def split_task(self, task):
        prompt = f"Divida a seguinte tarefa em subtarefas numeradas:\n{task}"
        response = self.assistant.llm(
            prompt, 
            max_tokens=CONFIG["model"]["max_tokens"],
            temperature=CONFIG["model"]["temperature"]
        )
        subtasks = re.findall(r"\d+\.\s+(.*)", response["choices"][0]["text"])

        log_debug(f"Subtarefas encontradas: {subtasks}", self.debug)
        return subtasks

    def execute_subtask(self, subtask):
        prompt = self.assistant.prompt_builder.generate_prompt(subtask)
        response = self.assistant.llm(
            prompt, 
            max_tokens=CONFIG["model"]["max_tokens"],
            temperature=CONFIG["model"]["temperature"]
        )
        cleaned_response = self.assistant.prompt_builder.clean_response(response['choices'][0]['text'])

        # Processa comandos e criação de arquivos se necessário
        if 'command:' in cleaned_response:
            command = self.assistant.command_executor.extract_command(cleaned_response)
            result = self.assistant.command_executor.execute_command(command)
            cleaned_response = cleaned_response.replace(f"{command}", result)

        if 'arquivo:' in cleaned_response:
            filename, content = self.extract_file(cleaned_response)
            self.create_file(filename, content)
            cleaned_response = f"Arquivo '{filename}' criado com sucesso. 📄"

        return cleaned_response

    def run_full_task(self, task):
        subtasks = self.split_task(task)
        
        if not subtasks:
            print("Nenhuma subtarefa identificada.")
            return
        
        with tqdm(total=len(subtasks), desc="Executando tarefas") as progress_bar:
            for subtask in subtasks:
                print(f"\nExecutando: {subtask}")
                result = self.execute_subtask(subtask)
                print(result)
                progress_bar.update(1)
