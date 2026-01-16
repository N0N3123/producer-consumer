"""
Flask API do monitorowania systemu producent-konsument.
Umożliwia dostęp do statystyk przez HTTP i WebSocket.
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Ścieżka do pliku ze statystykami
STATS_FILE = "stats.json"
LOG_FILE = "system.log"

# Cache dla aktualnych danych
_stats_cache = {
    "metadata": {},
    "statistics": {},
    "producers": [],
    "consumers": [],
    "last_update": None
}

def read_stats_file():
    """Czyta statystyki z pliku JSON"""
    global _stats_cache
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _stats_cache = data
                _stats_cache["last_update"] = datetime.now().isoformat()
                return data
    except Exception as e:
        print(f"[API] Błąd czytania stats: {e}")
    return _stats_cache

def read_log_file(lines=50):
    """Czyta ostatnie N linii z loga"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return [line.rstrip() for line in all_lines[-lines:]]
    except Exception as e:
        print(f"[API] Błąd czytania logu: {e}")
    return []

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Zwraca bieżące statystyki"""
    stats = read_stats_file()
    return jsonify(stats)

@app.route('/api/stats/live', methods=['GET'])
def get_live_stats():
    """Zwraca uproszczone live statystyki"""
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
    """Zwraca ostatnie logi"""
    lines = read_log_file(100)
    return jsonify({"logs": lines})

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/', methods=['GET'])
def dashboard():
    """Serwuje główny dashboard HTML"""
    return render_template('dashboard.html')


if __name__ == '__main__':
    print("[API] Uruchamianie Flask API na http://localhost:5000")
    print("[API] Otwórz http://localhost:5000 w przeglądarce")
    app.run(debug=False, host='0.0.0.0', port=5000)
