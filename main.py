"""
Główna orkestracja systemu producent-konsument.
Zarządza procesami producentów, konsumentów i monitora.
"""

import signal
import sys
import time
from multiprocessing import Process, Queue, Value, Lock, Manager

import config
from logger import init_logger, get_logger
from producer import Producer
from consumer import Consumer
from monitor import SystemMonitor


class ProducerConsumerSystem:

    def __init__(self):
        init_logger(
            log_file=config.LOG_FILE,
            to_file=config.LOG_TO_FILE,
            to_console=config.LOG_TO_CONSOLE
        )
        self.logger = get_logger()
        
        if config.PRIORITY_ENABLED:
            self.queue = Queue(maxsize=config.QUEUE_SIZE) 
            self.logger.info("SYSTEM", "Użyta Queue z priorytetami")
        else:
            self.queue = Queue(maxsize=config.QUEUE_SIZE)
            self.logger.info("SYSTEM", "Użyta zwykła Queue")
        self.produced_counter = Value('i', 0)
        self.consumed_counter = Value('i', 0)
        self.lock = Lock()
        
        self.manager = Manager()
        self.produced_items = self.manager.dict({i + 1: self.manager.list() for i in range(config.PRODUCERS_COUNT)})
        self.consumed_items = self.manager.dict({i + 1: self.manager.list() for i in range(config.CONSUMERS_COUNT)})
        
        self.producers: list[Process] = []
        self.consumers: list[Process] = []
        self.monitor: SystemMonitor = None
        self.last_monitor_time = time.time()

    def setup_signal_handlers(self) -> None:
        def signal_handler(sig, frame):
            self.logger.warning("SYSTEM", "Otrzymano sygnał przerwania")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def start(self) -> None:
        self.logger.info("SYSTEM", "=" * 60)
        self.logger.info("SYSTEM", "Uruchamianie systemu producent-konsument")
        self.logger.info("SYSTEM", f"Producenci: {config.PRODUCERS_COUNT}, Konsumenci: {config.CONSUMERS_COUNT}")
        self.logger.info("SYSTEM", f"Elementy per producent: {config.ITEMS_PER_PRODUCER}")
        self.logger.info("SYSTEM", f"Rozmiar kolejki: {config.QUEUE_SIZE}")
        self.logger.info("SYSTEM", "=" * 60)

        self.setup_signal_handlers()

        self.monitor = SystemMonitor(
            self.produced_counter,
            self.consumed_counter,
            self.queue,
            monitor_interval=config.MONITOR_INTERVAL,
            stats_file=config.STATS_FILE
        )
        self.logger.info("SYSTEM", "Monitor uruchomiony")
        for i in range(config.PRODUCERS_COUNT):
            producer = Producer(
                producer_id=i + 1,
                queue=self.queue,
                items_count=config.ITEMS_PER_PRODUCER,
                produced_counter=self.produced_counter,
                produced_items=self.produced_items,
                sleep_min=config.PRODUCER_SLEEP_MIN,
                sleep_max=config.PRODUCER_SLEEP_MAX,
                lock=self.lock
            )
            p = Process(target=producer.run)
            self.producers.append(p)
            p.start()
            self.logger.info("SYSTEM", f"Uruchomiono PRODUCENTA {i + 1}")

        for i in range(config.CONSUMERS_COUNT):
            consumer = Consumer(
                consumer_id=i + 1,
                queue=self.queue,
                consumed_counter=self.consumed_counter,
                consumed_items=self.consumed_items,
                sleep_min=config.CONSUMER_SLEEP_MIN,
                sleep_max=config.CONSUMER_SLEEP_MAX,
                lock=self.lock
            )
            c = Process(target=consumer.run)
            self.consumers.append(c)
            c.start()
            self.logger.info("SYSTEM", f"Uruchomiono KONSUMENTA {i + 1}")

        for p in self.producers:
            p.join(timeout=config.SHUTDOWN_TIMEOUT)
            if p.is_alive():
                self.logger.warning("SYSTEM", f"Producent {p.pid} nie zakończył się w time - terminate")
                p.terminate()

        self.logger.info("SYSTEM", "Wszyscy producenci zakończyli pracę")

        while self.consumed_counter.value < self.produced_counter.value:
            if time.time() - self.last_monitor_time >= config.MONITOR_INTERVAL:
                self.monitor.collect_stats()
                self.last_monitor_time = time.time()
            time.sleep(0.1)

        time.sleep(1)

        for _ in range(config.CONSUMERS_COUNT):
            self.queue.put(None)

        for c in self.consumers:
            c.join(timeout=config.SHUTDOWN_TIMEOUT)
            if c.is_alive():
                self.logger.warning("SYSTEM", f"Konsument {c.pid} nie zakończył się w time - terminate")
                c.terminate()

        self.logger.info("SYSTEM", "Wszyscy konsumenci zakończyli pracę")

    def shutdown(self) -> None:
        self.logger.info("SYSTEM", "Zamykanie systemu...")
        for p in self.producers:
            if p.is_alive():
                p.terminate()
        for c in self.consumers:
            if c.is_alive():
                c.terminate()

    def print_statistics(self) -> None:
        print("\n" + "=" * 60)
        print("FINALNE STATYSTYKI SYSTEMU")
        print("=" * 60)
        
        stats = self.monitor.get_final_stats()
        print(f"\n[OGOLNE]:")
        print(f"  Czas wykonania: {stats['total_time_seconds']} s")
        print(f"  Start: {stats['start_time']}")
        print(f"  Koniec: {stats['end_time']}")
        
        print(f"\n[PRODUKCJA I KONSUMPCJA]:")
        print(f"  Wyprodukowano: {stats['total_produced']} elementów")
        print(f"  Skonsumowano: {stats['total_consumed']} elementów")
        print(f"  W kolejce: {stats['items_in_queue']} elementów")
        
        print(f"\n[WYDAJNOSC]:")
        print(f"  Średnia przepustowość: {stats['average_throughput']} elem/s")
        print(f"  Efektywność: {stats['efficiency']}%")
        
        print(f"\n[PRODUKCJA PER PRODUCENT]:")
        for pid, items in self.produced_items.items():
            items_list = list(items)
            print(f"  Producent {pid}: {len(items_list)} elementów: {items_list}")
        
        print(f"\n[KONSUMPCJA PER KONSUMENT]:")
        for cid, items in self.consumed_items.items():
            items_list = list(items)
            print(f"  Konsument {cid}: {len(items_list)} elementów: {items_list}")
        
        print("\n" + "=" * 60)
        if config.EXPORT_STATS:
            self.monitor.export_stats(
                produced_items=self.produced_items,
                consumed_items=self.consumed_items
            )


def main():
    system = ProducerConsumerSystem()
    
    try:
        system.start()
    except KeyboardInterrupt:
        system.logger.info("SYSTEM", "Program przerwany przez użytkownika")
        system.shutdown()
    except Exception as e:
        system.logger.error("SYSTEM", f"Błąd krityczny: {e}")
        system.shutdown()
        raise
    
    system.print_statistics()
    system.logger.info("SYSTEM", "Program zakończył działanie")


if __name__ == "__main__":
    main()
