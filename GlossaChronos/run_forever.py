import subprocess
import time
import sys

def run_with_restart(script_name):
    while True:
        try:
            subprocess.run([sys.executable, script_name])
        except:
            print(f"Restarting {script_name}...")
            time.sleep(5)

if __name__ == "__main__":
    run_with_restart("text_fetcher.py")