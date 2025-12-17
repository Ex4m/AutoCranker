import sys
import json
import time
import os
import psutil
import subprocess
from datetime import datetime

SETTINGS_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'settings.json')


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        print(
            f"Settings file not found at {SETTINGS_FILE}. Please run gui.py first.")
        return None
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
        return None


def get_process_name(path):
    return os.path.basename(path)


def check_processes(exe_name, keywords):
    """
    Zkontroluje, zda běží jakýkoliv proces, který OBSAHUJE některé z klíčových slov.
    Vrací True, pokud takový proces existuje (což znamená 'blokováno').
    Vrací False, pokud je vše v pořádku (můžeme spustit).
    """
    if not keywords:
        return False

    print(f"Checking for processes containing keywords: {keywords}")

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            cmdline = proc.info['cmdline'] or []
            cmdline_str = " ".join(cmdline).lower()
            exe_path = (proc.info['exe'] or "").lower()

            for k in keywords:
                k_lower = k.lower()
                if k_lower in cmdline_str or k_lower in exe_path:
                    print(
                        f"BLOCKER FOUND: Process {proc.info['name']} (PID: {proc.info['pid']}) contains keyword '{k}'.")
                    return True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False  # Žádný blokující proces nenalezen


def run_app(path, interpreter=None):
    if interpreter:
        cmd = f'{interpreter} "{path}"'
        print(f"Starting application with interpreter: {cmd}")
    else:
        cmd = path
        print(f"Starting application: {cmd}")

    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print(f"Failed to start application: {e}")


def main():
    print("App Scheduler Runner started.")

    while True:
        settings = load_settings()
        if not settings:
            time.sleep(60)
            continue

        target_path = settings.get("target_path")
        interpreter = settings.get("interpreter")
        interval_val = settings.get("interval_value", 20)
        interval_unit = settings.get("interval_unit", "Minuty")
        keywords = settings.get("keywords", [])

        if not target_path or not os.path.exists(target_path):
            print(f"Target path invalid: {target_path}")
            time.sleep(60)
            continue

        # Calculate sleep time in seconds
        if interval_unit == "Hodiny":
            sleep_seconds = interval_val * 3600
        else:
            sleep_seconds = interval_val * 60

        exe_name = get_process_name(target_path)

        # Check logic
        is_blocked = check_processes(exe_name, keywords)

        if is_blocked:
            print(f"[{datetime.now()}] Launch blocked by existing process.")
        else:
            print(f"[{datetime.now()}] Launching application...")
            run_app(target_path, interpreter)

        print(f"Sleeping for {interval_val} {interval_unit}...")
        time.sleep(sleep_seconds)


if __name__ == '__main__':
    main()
