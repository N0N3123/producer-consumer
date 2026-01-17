QUEUE_SIZE: int = 50
PRODUCERS_COUNT: int = 3
CONSUMERS_COUNT: int = 5
ITEMS_PER_PRODUCER: int = 20

PRODUCER_SLEEP_MIN: float = 0.05
PRODUCER_SLEEP_MAX: float = 0.15

DEFECT_RATES: dict = {
    1: 0.05,
    2: 0.15,
    3: 0.08,
}

CONSUMER_SPEEDS: dict = {
    1: (0.08, 0.12),
    2: (0.25, 0.35),
    3: (0.45, 0.55),
    4: (0.85, 0.95),
    5: (0.6, 0.8),
}
SHUTDOWN_TIMEOUT: int = 30

LOG_FILE: str = "system.log"
LOG_TO_FILE: bool = True
LOG_TO_CONSOLE: bool = True
LOG_LEVEL: str = "INFO"

MONITOR_INTERVAL: float = 1.0
STATS_FILE: str = "stats.json"
EXPORT_STATS: bool = True

PRIORITY_ENABLED: bool = True
