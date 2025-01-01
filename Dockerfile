# Usar uma imagem base com Python
FROM python:3.9-slim

# Atualizar e instalar as dependências necessárias para o psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências do Python (incluindo psycopg2)
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Comando para rodar sua aplicação
CMD ["python", "projeto_nf/manage.py", "runserver", "0.0.0.0:8000"]

