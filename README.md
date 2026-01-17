# System Producent-Konsument z Dockerem

Prosta symulacja systemu produkcji z monitoringiem. Producenci generują przedmioty, konsumenci je przetwarzają, unikając przy tym przedmioty wadliwe, a dashboard pokazuje statystyki na żywo. Całość działa w kontenerze Dockera.

- **Python 3.12+** - (https://www.python.org/downloads/)

## 🚀 Uruchomienie

python run_docker.py

## 🏗️ Architektura

```
Producent-konsument/
├── main.py              # Główne działanie systemu
├── config.py            # Konfiguracja centralna
├── producer.py          # Klasa Producenta
├── consumer.py          # Klasa Konsumenta
├── monitor.py           # Monitoring i statystyki
├── logger.py            # System logowania
├── api.py               # Flask API dla dashboardu
├── templates/
│   └── dashboard.html   # Strona dashboardu
├── static/
│   ├── style.css        # Style dashboardu
│   └── script.js        # Logika dashboardu
├── requirements.txt     # Zależności Python
├── Dockerfile           # Konfiguracja Docker
├── docker-compose.yml   # Docker Compose config
├── .dockerignore        # Pliki ignorowane w Dockerze
├── run_docker.py        # Launcher (uruchamia Dockera)
└── README.md            # Dokumentacja
