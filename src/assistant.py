from colorama import Fore, Style, init
from config import CONFIG
from .model_loader import ModelLoader
from .prompt_builder import PromptBuilder
from .command_executor import CommandExecutor
from .task_executor import TaskExecutor
from .state_manager import StateManager
from .utils.logger import log_debug

class FranquinelsonAssistant:
    def __init__(self):
        self.debug = CONFIG["debug"]
        
        self.state_manager = StateManager(CONFIG["state"]["file"], self.debug)
        self.context = self.state_manager.load_state()

        self.llm = ModelLoader(debug=self.debug).load_model()

        self.prompt_builder = PromptBuilder(debug=self.debug)
        self.command_executor = CommandExecutor(debug=self.debug)
        self.task_executor = TaskExecutor(self, debug=self.debug)

    def chat(self):
        init(autoreset=True)
        print(Fore.GREEN + f"{CONFIG['name']} está online! Digite 'exit' para sair.")

        while True:
            user_input = input(Fore.CYAN + "Você: " + Style.RESET_ALL).strip()

            if user_input.lower() in ['exit', 'quit', 'sair', 'bye']:
                print(Fore.YELLOW + "Até logo! 😊")
                self.state_manager.save_state(self.context)
                break

            if user_input.lower().startswith("projeto:"):
                task = user_input[len("projeto:"):].strip()
                self.task_executor.run_full_task(task)
                continue

            prompt = self.prompt_builder.generate_prompt(user_input, self.context)

            log_debug("Gerando resposta", self.debug)

            response = self.llm(prompt, 
                                    max_tokens=CONFIG["model"]["max_tokens"],
                                    temperature=CONFIG["model"]["temperature"])
            
            cleaned_response = self.prompt_builder.clean_response(response['choices'][0]['text'])

            if 'command:' in cleaned_response:
                command = self.command_executor.extract_command(cleaned_response)
                command_result = self.command_executor.execute_command(command)
                cleaned_response = cleaned_response.replace(f"{command}", command_result)
                self.context = command_result
            else:
                self.context = None

            print(Fore.YELLOW + cleaned_response)
            self.state_manager.save_state(self.context)
