from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json
import os
import re
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

STATS_FILE = "stats.json"
LOG_FILE = "system.log"

_stats_cache = {
    "metadata": {},
    "statistics": {},
    "producers": [],
    "consumers": [],
    "last_update": None
}

def read_stats_file():
    global _stats_cache
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _stats_cache = data
                _stats_cache["last_update"] = datetime.now().isoformat()
                return data
    except Exception:
        pass
    return _stats_cache

def read_log_file(lines=50):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return [line.rstrip() for line in all_lines[-lines:]]
    except Exception:
        pass
    return []

def parse_producers_and_consumers_from_logs():
    producers = {}
    consumers = {}
    
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    prod_match = re.search(r'PRODUCENT (\d+).*Wyprodukowano: (\d+)', line)
                    if prod_match:
                        pid = int(prod_match.group(1))
                        item = int(prod_match.group(2))
                        if pid not in producers:
                            producers[pid] = []
                        producers[pid].append(item)
                    
                    cons_match = re.search(r'KONSUMENT (\d+).*Przetwarzam: (\d+)', line)
                    if cons_match:
                        cid = int(cons_match.group(1))
                        item = int(cons_match.group(2))
                        if cid not in consumers:
                            consumers[cid] = []
                        consumers[cid].append(item)
    except Exception:
        pass
    
    return producers, consumers

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = read_stats_file()
    producers, consumers = parse_producers_and_consumers_from_logs()
    
    producers_list = []
    for pid in sorted(producers.keys()):
        items = producers[pid]
        producers_list.append({
            "id": pid,
            "count": len(items),
            "items": items
        })
    
    consumers_list = []
    for cid in sorted(consumers.keys()):
        items = consumers[cid]
        consumers_list.append({
            "id": cid,
            "count": len(items),
            "items": items
        })
    
    stats["producers"] = producers_list
    stats["consumers"] = consumers_list
    
    return jsonify(stats)

@app.route('/api/stats/live', methods=['GET'])
def get_live_stats():
    stats = read_stats_file()
    return jsonify({
        "produced": stats.get("statistics", {}).get("total_produced", 0),
        "consumed": stats.get("statistics", {}).get("total_consumed", 0),
        "efficiency": stats.get("statistics", {}).get("efficiency_percent", 0),
        "throughput": stats.get("statistics", {}).get("average_throughput_per_sec", 0),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/logs', methods=['GET'])
def get_logs():
    lines = read_log_file(100)
    return jsonify({"logs": lines})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
