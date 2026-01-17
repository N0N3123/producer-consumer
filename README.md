# System Producent-Konsument z Dockerem

Prosta symulacja systemu produkcji z monitoringiem. Producenci generują przedmioty, konsumenci je przetwarzają, unikając przy tym przedmioty wadliwe, a dashboard pokazuje statystyki na żywo. Całość działa w kontenerze Dockera.

## 📋 Cel Projektu

System demonstruje:
- **Architekturę producent-konsument** z wieloprocesową synchronizacją
- **Symulację produkcji** z wadliwymi produktami
- **Monitoring real-time** z zapisywaniem statystyk do JSON
- **Dashboard web** pokazujący statystyki
- **Dockeryzację** aplikacji z automatycznym otwarciem przeglądarki

## 🛠️ Zastosowane Rozwiązania

### Backend
- **Python 3.12** z multiprocessingiem (`Queue`, `Value`, `Lock`, `Manager`)
- **Flask 3.0.0** z CORS dla REST API
- System logowania z timestamp'ami
- Monitoring i eksport statystyk do JSON (aktualizacja real-time)

### Frontend
- **HTML5 + CSS3**
- **Chart.js**
- **Vanilla JavaScript**

### Docker
## 🚀 Wymagania

- **Python 3.12+**
- **Docker Desktop**

## 🚀 Uruchomienie
```bash
python run_docker.py
```
## 📊 Jak to Działa

1. **Producenci** (3 procesy) - Generują 20 przedmiotów każdy
   - Producent 1: 5% wad
   - Producent 2: 15% wad
   - Producent 3: 8% wad

2. **Konsumenci** (5 procesów) - Przetwarzają z różnymi szybkościami
   - Odrzucają wadliwe produkty
   - Liczą tylko prawidłowe jako "skonsumowane"

3. **Monitor** - Zbiera statystyki co 1 sekundę, pisze do `stats.json`

4. **Dashboard** - Pokazuje:
   - Liczba wyprodukowanych przedmiotów
   - Liczba skonsumowanych (bez wadliwych)
   - Efektywność (%)
   - Liczba wadliwych produktów
   - Wykres trendu konsumpcji
   - Logi systemu

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
├── .gitignore           # Pliki ignorowane przez Git
└── README.md            # Dokumentacja
```
