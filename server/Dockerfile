# Folosim o imagine oficială de Linux (foarte ușoară) cu Python preinstalat
FROM python:3.11-slim

# Setăm folderul de lucru în interiorul containerului
WORKDIR /app

# Copiem fișierul cu dependențe din laptop în container
COPY requirements.txt .

# Instalăm librăriile
RUN pip install --no-cache-dir -r requirements.txt

# Copiem tot codul serverului (main.py) în container
COPY . .

# Anunțăm că acest container va emite și primi trafic pe portul 8000
EXPOSE 8000

# Comanda care va ține containerul aprins (pornește dispecerul FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]