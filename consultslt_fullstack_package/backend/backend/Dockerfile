FROM python:3.11-slim

WORKDIR /app

# Copia dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend
COPY . .

# Comando para iniciar o backend
CMD ["uvicorn", "main_enterprise:app", "--host", "0.0.0.0", "--port", "8000"]
