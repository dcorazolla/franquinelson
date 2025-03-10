# 🧠 Franquinelson - Assistente IA 🚀

**Franquinelson** é um assistente virtual desenvolvido para ajudar programadores e tech leads no dia a dia, fornecendo suporte em comandos do sistema operacional, automação de tarefas e geração de código.

---

## 📌 Recursos Principais

✅ Conversa natural e contextual em **português**  
✅ Executa **comandos seguros** no sistema operacional  
✅ Automatiza tarefas complexas, **dividindo-as em subtarefas**  
✅ **Persistência de estado** (continua de onde parou)  
✅ **Executa dentro de um container Docker**  
✅ **Carregamento otimizado de modelos** para melhor desempenho  
✅ **Testes unitários completos** com `pytest` e cobertura de código  

---

## 🛠️ Requisitos

Antes de instalar, verifique se você tem:

- **Docker** e **Docker Compose** instalados (se deseja rodar em container)
- **Python 3.9 ou superior** (caso prefira rodar localmente)
- Pelo menos **8GB de RAM** para um bom desempenho do modelo  
- **Espaço livre em disco:** O modelo pode ocupar **2GB+**  

---

## 🚀 Instalação e Execução

### 📌 **Rodando via Docker (Recomendado)**

1️⃣ **Clone o repositório**:

```bash
git clone https://github.com/dcorazolla/franquinelson.git
cd franquinelson
```

2️⃣ Construa e inicie o container:

```bash
docker-compose up --build -d
```

3️⃣ Acesse o container via SSH:

```bash
ssh root@localhost -p 2222  # Senha: docker
```

4️⃣ Inicie o assistente manualmente:

```bash
cd /app
python main.py
```

📌 Rodando localmente (sem Docker)

1️⃣ Instale as dependências:

```bash
pip install -r requirements.txt
```

2️⃣ Inicie o assistente:

```bash
python main.py
```

📝 Comandos e Interações  

📢 Exemplos de Interação  

```bash
Você: Qual o seu nome?
Franquinelson: E aí! Eu sou o Franquinelson, o assistente tech caipira! 🤠 Como posso te ajudar?
```
```bash
Você: Execute comando: {command: date}
Franquinelson: Opa! Aqui tá o dia e hora atual: Ter 10 Mar 2025 15:40:12 BRT
```
```bash
Você: Projeto: Crie um site simples com HTML, CSS e um menu superior.
Franquinelson: Beleza! Vamos dividir essa tarefa:
1️⃣ Criando estrutura base do projeto...
2️⃣ Gerando `index.html`...
3️⃣ Criando `styles.css`...
...
✅ Site pronto!
```


🔍 Como o Assistente Funciona?  

🏗 Fluxo de Execução  

O usuário faz uma pergunta (via texto ou comando).  
O assistente interpreta o pedido e decide:  
Responder normalmente OU  
Executar um comando do sistema OU  
Criar e gerenciar arquivos OU  
Dividir a tarefa em subtarefas e executar cada uma.  
Se necessário, interage com o sistema operacional.  
Retorna a resposta formatada para o usuário.  

📂 Estrutura do Projeto  

```bash
franquinelson/
├── Dockerfile              # Configuração do ambiente Docker
├── docker-compose.yml      # Configuração do Docker Compose
├── requirements.txt        # Dependências do projeto
├── config.py               # Configurações gerais do assistente
├── src/
│   ├── assistant.py        # Gerencia a interação com o usuário
│   ├── main.py             # Arquivo principal que inicia o assistente
│   ├── model_loader.py     # Carrega e verifica o modelo de IA
│   ├── prompt_builder.py   # Formata as perguntas para o modelo
│   ├── command_executor.py # Executa comandos do sistema operacional
│   ├── state_manager.py    # Gerencia persistência de contexto
│   ├── task_executor.py    # Divide e executa tarefas complexas
│   └── utils/
│       ├── logger.py       # Logger para debug
│       └── __init__.py
└── tests/                  # Testes unitários
    ├── test_assistant.py
    ├── test_model_loader.py
    ├── test_command_executor.py
    ├── test_state_manager.py
    ├── test_task_executor.py
    └── test_prompt_builder.py
```

🧪 Rodando os Testes  

Para garantir que tudo está funcionando corretamente, rode:

```bash
pytest tests/ --verbose --cov=src --cov-report=term-missing
```
Isso executará todos os testes e mostrará a cobertura do código.

📜 Licença
Este projeto está licenciado sob a MIT License.

🏆 Contribuição
Se quiser contribuir, abra uma Issue ou envie um Pull Request! 🚀

