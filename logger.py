"""
System zaawansowanego loggowania do konsoli i pliku.
"""

from datetime import datetime
from typing import Optional
from pathlib import Path


class Logger:
    def __init__(self, log_file: Optional[str] = None, to_file: bool = True, to_console: bool = True):
        self.log_file = log_file
        self.to_file = to_file
        self.to_console = to_console
        
        if self.log_file and self.to_file:
            Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, 'w') as f:
                f.write("")

    def _format_message(self, prefix: str, message: str) -> str:
        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return f"[{now}] [{prefix:20}] {message}"

    def log(self, prefix: str, message: str) -> None:
        formatted = self._format_message(prefix, message)
        
        if self.to_console:
            print(formatted, flush=True)
        
        if self.to_file and self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(formatted + '\n')

    def info(self, prefix: str, message: str) -> None:
        self.log(f"[INFO] {prefix}", message)

    def warning(self, prefix: str, message: str) -> None:
        self.log(f"[WARN] {prefix}", message)

    def error(self, prefix: str, message: str) -> None:
        self.log(f"[ERR] {prefix}", message)

    def debug(self, prefix: str, message: str) -> None:
        self.log(f"[DBG] {prefix}", message)


_logger: Optional[Logger] = None


def get_logger() -> Logger:
    global _logger
    if _logger is None:
        raise RuntimeError("Logger nie został zainicjalizowany. Użyj init_logger() najpierw.")
    return _logger


def init_logger(log_file: Optional[str] = None, to_file: bool = True, to_console: bool = True) -> Logger:
    global _logger
    _logger = Logger(log_file, to_file, to_console)
    return _logger
