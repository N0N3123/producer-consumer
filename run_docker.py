import subprocess
import shutil
import webbrowser
import threading
import time


def pick_compose_command() -> list[str]:
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    return ["docker", "compose"]


def open_browser_delayed(url: str, delay: int = 2):
    def _open():
        time.sleep(delay)
        webbrowser.open(url)
    
    thread = threading.Thread(target=_open, daemon=True)
    thread.start()


def main() -> None:
    compose_cmd = pick_compose_command()
    cmd = compose_cmd + ["up", "--build"]
    dashboard_url = "http://localhost:5000"
    
    open_browser_delayed(dashboard_url, delay=4)
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
