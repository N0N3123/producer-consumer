FROM python:3.12-slim

WORKDIR /app

# Zainstaluj zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj wszystkie pliki projektu
COPY . .

# Expose port dla Flask API
EXPOSE 5000

# Uruchom system producent-konsument w tle i Flask API
CMD python main.py & python api.py
