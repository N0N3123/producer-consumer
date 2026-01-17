import time
from multiprocessing import Queue, Value, Lock
from logger import get_logger


class Consumer:
    def __init__(self,
                 consumer_id: int,
                 queue: Queue,
                 consumed_counter: Value,
                 consumed_items: dict,
                 sleep_min: float = 0.7,
                 sleep_max: float = 1.2,
                 lock: Lock = None):
        self.consumer_id = consumer_id
        self.queue = queue
        self.consumed_counter = consumed_counter
        self.consumed_items = consumed_items
        self.sleep_min = sleep_min
        self.sleep_max = sleep_max
        self.lock = lock
        self.logger = get_logger()

    def consume(self) -> None:
        self.logger.info(f"KONSUMENT {self.consumer_id}", "Rozpoczęto konsumpcję")
        
        items_processed = 0
        items_rejected = 0
        try:
            while True:
                item_tuple = self.queue.get()
                
                if item_tuple is None:
                    self.logger.info(f"KONSUMENT {self.consumer_id}", "Otrzymano sygnał STOP")
                    break
                
                priority, item, is_defective = item_tuple
                
                if is_defective:
                    items_rejected += 1
                    self.logger.info(
                        f"KONSUMENT {self.consumer_id}",
                        f"ODRZUCONO WADLIWY: {item} (odrzuconych: {items_rejected})"
                    )
                    continue
                
                with self.lock:
                    self.consumed_counter.value += 1
                    self.consumed_items[self.consumer_id].append(item)
                
                items_processed += 1
                
                self.logger.info(
                    f"KONSUMENT {self.consumer_id}",
                    f"Przetwarzam: {item} (priorytet: {priority}, przetworzonych: {items_processed})"
                )
                
                time.sleep(self.sleep_min + (self.sleep_max - self.sleep_min) * (priority / 2))
        
        except Exception as e:
            self.logger.error(f"KONSUMENT {self.consumer_id}", f"Błąd: {e}")
        
        self.logger.info(f"KONSUMENT {self.consumer_id}", f"Zakończył pracę (przetworzył: {items_processed})")

    def run(self) -> None:
        self.consume()
