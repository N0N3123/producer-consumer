"""
Konfiguracja systemu producent-konsument.
Centralne miejsce dla wszystkich parametrów.
"""

# ============ Parametry systemu ============
QUEUE_SIZE: int = 5
PRODUCERS_COUNT: int = 3
CONSUMERS_COUNT: int = 2
ITEMS_PER_PRODUCER: int = 6

# ============ Timeouty ============
PRODUCER_SLEEP_MIN: float = 0.2
PRODUCER_SLEEP_MAX: float = 0.6
CONSUMER_SLEEP_MIN: float = 0.7
CONSUMER_SLEEP_MAX: float = 1.2
SHUTDOWN_TIMEOUT: int = 30

# ============ Logging ============
LOG_FILE: str = "system.log"
LOG_TO_FILE: bool = True
LOG_TO_CONSOLE: bool = True
LOG_LEVEL: str = "INFO"

# ============ Monitoring ============
MONITOR_INTERVAL: float = 1.0
STATS_FILE: str = "stats.json"
EXPORT_STATS: bool = True

# ============ Priorytet elementy ============
PRIORITY_ENABLED: bool = True
