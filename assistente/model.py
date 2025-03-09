import os
import requests
from tqdm import tqdm
from .config import CONFIG

def verify():
    """Verifica se o modelo existe na pasta 'models'"""
    complete_path = os.path.join(CONFIG["model"]["path"], CONFIG["model"]["file"])

    if os.path.exists(complete_path):
        print(f"\nModelo encontrado: {complete_path}")
        return True
    else:
        print(f"\nModelo não encontrado.")
        return download(complete_path)
    

def download(complete_path):
    """Baixa o modelo para a pasta 'models'"""
    os.makedirs(CONFIG["model"]["path"], exist_ok=True)

    print(f"\nBaixando modelo...")

    try:
        with requests.get(CONFIG["model"]["url"], stream=True, verify=False) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

            with open(complete_path, 'wb') as f, tqdm(
                desc=CONFIG["model"]["file"],
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"Download concluído: {complete_path}")
        return True
    
    except Exception as e:
        print(f"Erro ao baixar o modelo: {e}")
        return False