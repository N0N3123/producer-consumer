# System Producent-Konsument z Programowaniem Równoległym

Zaawansowany projekt uniwersytecki implementujący wzorzec producent-konsument z wykorzystaniem programowania równoległego w Pythonie oraz web dashboard do monitorowania w czasie rzeczywistym.

- **Python 3.12+** - (https://www.python.org/downloads/)

## 📦 Instalacja

### Metoda 1: Automatyczna


## 🚀 Uruchomienie

### Sposób 1: Lokalnie (Windows)



To otworzy 2 terminale:

1. **Terminal 1** - System producent-konsument (`main.py`)
2. **Terminal 2** - Web dashboard API (`api.py`)

Następnie otwórz w przeglądarce: **http://localhost:5000**

### Sposób 2: Ręcznie (2 terminale)

**Terminal 1:**

```bash
python main.py
```

**Terminal 2:**

```bash
python api.py
```

Otwórz przeglądarkę: **http://localhost:5000**

### Sposób 3: Docker (NAJŁATWIEJSZY)

```bash
# Upewnij się że Docker Desktop jest uruchomiony!

# Kliknij dwukrotnie:
run_docker.bat

# Lub ręcznie:
docker-compose up --build
```

Otwórz przeglądarkę: **http://localhost:5000**

**Zatrzymanie Docker:**

```bash
Ctrl+C
# Lub
docker-compose down
```

---

## 🏗️ Architektura

```
Producent-konsument/
├── main.py              # Główna orkestracja systemu
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
├── setup.bat            # Skrypt instalacyjny (Windows)
├── run_local.bat        # Uruchomienie lokalne (Windows)
├── run_docker.bat       # Uruchomienie Docker (Windows)
└── README.md            # Ta dokumentacja
```

---

## 🎯 Jak Działa Program

### 1. **Producenci** (3 procesy równoległe)

- Generują losowe liczby od 1 do 100
- Przypisują priorytet: wartość > 80 = priorytet 1 (wysoki), reszta = priorytet 0
- Wstawiają do kolejki jako tuple: `(priorytet, wartość)`
- Każdy producent generuje 6 elementów

### 2. **Kolejka** (wspólny bufor)

- Maksymalny rozmiar: 5 elementów
- Jeśli pełna, producent czeka (blokuje się)
- Bezpieczna komunikacja między procesami (IPC)

### 3. **Konsumenci** (2 procesy równoległe)

- Pobierają elementy z kolejki (FIFO)
- Elementy o wyższym priorytecie są przetwarzane szybciej
- Każdy konsument przetwarza ~9 elementów

### 4. **Synchronizacja**

- **Lock** - Chroni liczniki przed race condition
- **Value** - Współdzielone liczniki (wyprodukowane/skonsumowane)
- **Manager** - Zarządza współdzielonymi listami elementów

### 5. **Monitoring**

- Co 1 sekundę zbiera statystyki
- Eksportuje wyniki do `stats.json`
- Loguje wszystkie zdarzenia do `system.log`

### 6. **Web Dashboard**

- Flask API udostępnia endpoint `/api/stats`
- JavaScript odświeża dane co 1 sekundę
- Pokazuje live: wyprodukowane, skonsumowane, efektywność, logi

---

## ⚙️ Konfiguracja

Edytuj plik **`config.py`**:

```python
# Liczba procesów
PRODUCERS_COUNT = 3          # Ile producentów
CONSUMERS_COUNT = 2          # Ile konsumentów
ITEMS_PER_PRODUCER = 6       # Ile każdy producent wyprodukuje

# Kolejka
QUEUE_SIZE = 5               # Max rozmiar kolejki

# Timeouty (sekundy)
PRODUCER_SLEEP_MIN = 0.2     # Min czas między produkcją
PRODUCER_SLEEP_MAX = 0.6     # Max czas między produkcją
CONSUMER_SLEEP_MIN = 0.7     # Min czas przetwarzania
CONSUMER_SLEEP_MAX = 1.2     # Max czas przetwarzania

# Monitoring
MONITOR_INTERVAL = 1.0       # Co ile sekund zbierać statystyki

# Priorytety
PRIORITY_ENABLED = True      # Czy używać priorytetów
```

---

## 🖥️ Web Dashboard

Dashboard dostępny pod adresem **http://localhost:5000** 
