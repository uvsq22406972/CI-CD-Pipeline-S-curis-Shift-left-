FROM python:3.12-slim

#Empêche Python de créer des .pyc et force l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Copier le projet dans /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#Copie tout le repo (donc /app/app/app.py existe)
COPY . .

#Se placer dans le dossier contenant app.py + instance/
WORKDIR /app/app

#S'assurer que le dossier existe
RUN mkdir -p instance

EXPOSE 8080
USER non-root CMD ["python", "app.py"]
