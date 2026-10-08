# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências primeiro (otimização de cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte e arquivos necessários
COPY src/ ./src/

# Define a variável de ambiente para unbuffer no stdout/stderr (logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Comando padrão para executar o componente
CMD ["python", "src/main.py"]