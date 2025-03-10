FROM python:3.9-slim

# Define variáveis de ambiente para desempenho otimizado
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala pacotes necessários
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    supervisor \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configura SSH (senha: docker)
RUN mkdir /var/run/sshd \
    && echo 'root:docker' | chpasswd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Diretório principal da aplicação
WORKDIR /app

# Copia e instala dependências Python com trusted-host
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.org \
                --trusted-host files.pythonhosted.org \
                --trusted-host pypi.python.org \
                --no-cache-dir -r requirements.txt

# Supervisor para rodar serviços
RUN mkdir -p /var/log/supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Porta SSH
EXPOSE 22

# Inicia Supervisor
CMD ["/usr/bin/supervisord", "-n"]
