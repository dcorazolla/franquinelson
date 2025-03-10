import subprocess
import shlex
from tqdm import tqdm
from .utils.logger import log_debug


class CommandExecutor:
    ALLOWED_COMMANDS = {
        'ls': ['ls', '-l'],
        'pwd': ['pwd'],
        'date': ['date'],
        'free': ['free', '-h'],
        'df': ['df', '-h'],
        'uname': ['uname', '-a']
    }

    def __init__(self, debug=False):
        self.debug = debug

    def extract_command(self, response_text):
        start = response_text.find('command:')
        if start == -1:
            return None
        end = response_text.find('}', start)
        if end == -1:
            return None
        command_text = response_text[start + len('command:'):end].strip()
        log_debug(f"Comando extraído: {command_text}", self.debug)
        return command_text

    def execute_command(self, command):
        cmd_parts = shlex.split(command)
        base_cmd = cmd_parts[0]

        if base_cmd not in self.ALLOWED_COMMANDS:
            log_debug(f"Tentativa de comando não permitido: {base_cmd}", self.debug)
            return "Erro: comando não permitido 🚫"

        safe_command = self.ALLOWED_COMMANDS[base_cmd] + cmd_parts[1:]

        try:
            with tqdm(total=1, desc=f"Executando: {base_cmd}", unit="cmd") as progress_bar:
                result = subprocess.run(
                    safe_command,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=True
                )
                progress_bar.update(1)
                output = result.stdout.strip() or result.stderr.strip()
                log_debug(f"Comando executado com sucesso: {command}", self.debug)
                return output

        except subprocess.CalledProcessError as e:
            log_debug(f"Erro no comando: {command} | {e}", self.debug)
            return f"Erro ao executar comando: {e.stderr.strip()} ❌"

        except subprocess.TimeoutExpired:
            log_debug(f"Timeout do comando: {command}", self.debug)
            return "Erro: tempo limite excedido para execução do comando ⌛️"
