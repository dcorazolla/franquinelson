import subprocess
from typing import Tuple
from .debug import log_debug

# Whitelist de comandos permitidos
COMANDOS_PERMITIDOS = {
    'ls': ['ls', '-l'],
    'pwd': ['pwd'],
    'date': ['date'],
    'echo': ['echo'],
    'uname': ['uname', '-a'],
    'df': ['df', '-h'],
    'free': ['free', '-h'],
    'node': ['node', '-v']
}

def executar_comando_seguro(comando: str) -> Tuple[str, bool]:
    partes = comando.split()
    base_cmd = partes[0] if partes else ''
    if base_cmd not in COMANDOS_PERMITIDOS:
        return f"Erro: Comando '{base_cmd}' não permitido!", False
    try:
        resultado = subprocess.run(
            COMANDOS_PERMITIDOS[base_cmd] + partes[1:],
            capture_output=True,
            text=True,
            timeout=5
        )
        log_debug(f"Executado comando: {comando} | Resultado: {resultado.stdout.strip() or resultado.stderr.strip()}")
        return (resultado.stdout if resultado.stdout else resultado.stderr, True)
    except Exception as e:
        log_debug(f"Erro ao executar comando: {comando} | {str(e)}")
        return f"Erro executando comando: {str(e)}", False
