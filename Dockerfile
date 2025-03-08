FROM python:3.9-slim

# Instalar pacotes necessários: SSH, Supervisor, e ferramentas de compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    supervisor \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configurar o SSH
RUN mkdir /var/run/sshd && \
    echo 'root:docker' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório para logs do Supervisor
RUN mkdir -p /var/log/supervisor

# Copiar configuração do Supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expor a porta SSH
EXPOSE 22

# Iniciar o Supervisor que gerencia o SSH e o assistente
CMD ["/usr/bin/supervisord", "-n"]
