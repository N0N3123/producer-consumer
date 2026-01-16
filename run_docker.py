"""
Uruchamia projekt w Dockerze i automatycznie otwiera dashboard w przeglądarce.
Użycie: python run_docker.py
"""

import subprocess
import sys
import shutil
import webbrowser
import threading
import time


def ensure_docker_available() -> None:
    if shutil.which("docker") is None:
        print("[BŁĄD] Docker nie jest zainstalowany lub nie jest w PATH.")
        print("       Pobierz Docker Desktop: https://www.docker.com/products/docker-desktop/")
        sys.exit(1)


def pick_compose_command() -> list[str]:
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    if shutil.which("docker"):
        return ["docker", "compose"]
    print("[BŁĄD] Nie znaleziono docker ani docker-compose w PATH.")
    sys.exit(1)


def open_browser_delayed(url: str, delay: int = 8):
    """Otwórz przeglądarkę po opóźnieniu (aby dać czas kontenerom na start)"""
    def _open():
        time.sleep(delay)
        print(f"\n{'='*60}")
        print(f"  🌐 Otwieranie dashboardu: {url}")
        print(f"{'='*60}\n")
        webbrowser.open(url)
    
    thread = threading.Thread(target=_open, daemon=True)
    thread.start()


def main() -> None:
    print("="*60)
    print("  Uruchamianie Systemu Producent-Konsument w Docker")
    print("="*60)
    print()
    
    ensure_docker_available()
    compose_cmd = pick_compose_command()

    cmd = compose_cmd + ["up", "--build"]
    dashboard_url = "http://localhost:5000"
    
    print(f"[INFO] Uruchamiam: {' '.join(cmd)}")
    print(f"[INFO] Dashboard będzie dostępny pod: {dashboard_url}")
    print(f"[INFO] Przeglądarka otworzy się automatycznie za ~8 sekund")
    print(f"[INFO] Przerwij Ctrl+C aby zatrzymać kontenery")
    print()
    
    # Uruchom timer do otworzenia przeglądarki
    open_browser_delayed(dashboard_url)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"\n[BŁĄD] Polecenie zakończone błędem (kod {exc.returncode}).")
        sys.exit(exc.returncode)
    except KeyboardInterrupt:
        print("\n\n[INFO] Przerwano przez użytkownika.")
        print("[INFO] Zatrzymywanie kontenerów...")
    finally:
        pass


if __name__ == "__main__":
    main()
