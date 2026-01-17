import json
import time
from multiprocessing import Value, Queue
from typing import Dict, Any
from datetime import datetime


class SystemMonitor:

    def __init__(self, 
                 produced_counter: Value,
                 consumed_counter: Value,
                 queue: Queue,
                 monitor_interval: float = 1.0,
                 stats_file: str = "stats.json"):
        self.produced_counter = produced_counter
        self.consumed_counter = consumed_counter
        self.queue = queue
        self.monitor_interval = monitor_interval
        self.stats_file = stats_file
        self.start_time = time.time()
        self.history: list[Dict[str, Any]] = []

    def get_stats(self) -> Dict[str, Any]:
        elapsed = time.time() - self.start_time
        produced = self.produced_counter.value
        consumed = self.consumed_counter.value
        queue_size = self.queue.qsize()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": round(elapsed, 2),
            "produced": produced,
            "consumed": consumed,
            "queue_size": queue_size,
            "throughput_per_sec": round(produced / elapsed if elapsed > 0 else 0, 2),
            "lag": produced - consumed
        }

    def _update_stats_file(self) -> None:
        try:
            elapsed = time.time() - self.start_time
            produced = self.produced_counter.value
            consumed = self.consumed_counter.value
            
            stats_data = {
                "metadata": {
                    "total_time_seconds": round(elapsed, 2),
                    "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                    "end_time": datetime.now().isoformat()
                },
                "statistics": {
                    "total_produced": produced,
                    "total_consumed": consumed,
                    "average_throughput_per_sec": round(produced / elapsed if elapsed > 0 else 0, 2),
                    "efficiency_percent": round((consumed / produced * 100) if produced > 0 else 0, 2)
                },
                "producers": [],
                "consumers": []
            }
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def collect_stats(self) -> None:
        stats = self.get_stats()
        self.history.append(stats)
        self._update_stats_file()

    def export_stats(self, produced_items: dict = None, consumed_items: dict = None) -> None:
        try:
            final_stats = self.get_final_stats()
            producers_list = []
            consumers_list = []
            
            if produced_items:
                for pid in sorted(produced_items.keys()):
                    items = list(produced_items[pid])
                    producers_list.append({
                        "id": pid,
                        "count": len(items),
                        "items": items
                    })
            
            if consumed_items:
                for cid in sorted(consumed_items.keys()):
                    items = list(consumed_items[cid])
                    consumers_list.append({
                        "id": cid,
                        "count": len(items),
                        "items": items
                    })
            
            export_data = {
                "metadata": {
                    "total_time_seconds": final_stats['total_time_seconds'],
                    "start_time": final_stats['start_time'],
                    "end_time": final_stats['end_time']
                },
                "statistics": {
                    "total_produced": final_stats['total_produced'],
                    "total_consumed": final_stats['total_consumed'],
                    "average_throughput_per_sec": final_stats['average_throughput'],
                    "efficiency_percent": final_stats['efficiency']
                },
                "producers": producers_list,
                "consumers": consumers_list
            }
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                lines = ['{']
                lines.append('  "metadata": {')
                lines.append(f'    "total_time_seconds": {export_data["metadata"]["total_time_seconds"]},')
                lines.append(f'    "start_time": "{export_data["metadata"]["start_time"]}",')
                lines.append(f'    "end_time": "{export_data["metadata"]["end_time"]}"')
                lines.append('  },')
                
                lines.append('  "statistics": {')
                stats = export_data["statistics"]
                lines.append(f'    "total_produced": {stats["total_produced"]},')
                lines.append(f'    "total_consumed": {stats["total_consumed"]},')
                lines.append(f'    "average_throughput_per_sec": {stats["average_throughput_per_sec"]},')
                lines.append(f'    "efficiency_percent": {stats["efficiency_percent"]}')
                lines.append('  },')
                
                lines.append('  "producers": [')
                for i, prod in enumerate(export_data["producers"]):
                    items_str = ', '.join(str(x) for x in prod["items"])
                    lines.append(f'    {{"id": {prod["id"]}, "count": {prod["count"]}, "items": [{items_str}]}}' + (',' if i < len(export_data["producers"]) - 1 else ''))
                lines.append('  ],')
                
                lines.append('  "consumers": [')
                for i, cons in enumerate(export_data["consumers"]):
                    items_str = ', '.join(str(x) for x in cons["items"])
                    lines.append(f'    {{"id": {cons["id"]}, "count": {cons["count"]}, "items": [{items_str}]}}' + (',' if i < len(export_data["consumers"]) - 1 else ''))
                lines.append('  ]')
                
                lines.append('}')
                f.write('\n'.join(lines))
            print(f"[MONITOR] Statystyki eksportowane do {self.stats_file}")
        except Exception as e:
            print(f"[MONITOR] Błąd eksportu statystyk: {e}")

    def get_final_stats(self) -> Dict[str, Any]:
        elapsed = time.time() - self.start_time
        produced = self.produced_counter.value
        consumed = self.consumed_counter.value
        
        return {
            "total_time_seconds": round(elapsed, 2),
            "total_produced": produced,
            "total_consumed": consumed,
            "average_throughput": round(produced / elapsed if elapsed > 0 else 0, 2),
            "efficiency": round((consumed / produced * 100) if produced > 0 else 0, 2),
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.now().isoformat()
        }
