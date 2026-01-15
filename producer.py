"""
Klasa Producenta w systemie producent-konsument.
"""

import time
import random
from multiprocessing import Queue, Value, Lock
from logger import get_logger


class Producer:

    def __init__(self,
                 producer_id: int,
                 queue: Queue,
                 items_count: int,
                 produced_counter: Value,
                 produced_items: dict,
                 sleep_min: float = 0.2,
                 sleep_max: float = 0.6,
                 lock: Lock = None):
        self.producer_id = producer_id
        self.queue = queue
        self.items_count = items_count
        self.produced_counter = produced_counter
        self.produced_items = produced_items
        self.sleep_min = sleep_min
        self.sleep_max = sleep_max
        self.lock = lock
        self.logger = get_logger()

    def produce(self) -> None:
        self.logger.info(f"PRODUCENT {self.producer_id}", "Rozpoczęto produkcję")
        
        for i in range(self.items_count):
            try:
                item = random.randint(1, 100)
                priority = 0 
                if item > 80:
                    priority = 1
                
                self.queue.put((priority, item))
                
                with self.lock:
                    self.produced_counter.value += 1
                    self.produced_items[self.producer_id].append(item)
                
                self.logger.info(
                    f"PRODUCENT {self.producer_id}",
                    f"Wyprodukowano: {item} (priorytet: {priority}, postęp: {i + 1}/{self.items_count})"
                )
                
                time.sleep(random.uniform(self.sleep_min, self.sleep_max))
            
            except Exception as e:
                self.logger.error(f"PRODUCENT {self.producer_id}", f"Błąd: {e}")

        self.logger.info(f"PRODUCENT {self.producer_id}", "Zakończył pracę")

    def run(self) -> None:
        self.produce()
