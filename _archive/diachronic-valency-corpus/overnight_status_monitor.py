import time
import os
from datetime import datetime

STATUS_FILE = "overnight_status.txt"

# Simple status monitor for the super platform

def get_status():
    # Check for unhealthy containers
    unhealthy = os.popen("docker ps --filter 'health=unhealthy' --format '{{.Names}}'").read().strip().splitlines()
    # Check for error logs
    error_log = "overnight_errors.log"
    errors = []
    if os.path.exists(error_log):
        with open(error_log, encoding="utf-8") as f:
            errors = f.readlines()[-5:]
    return unhealthy, errors

def write_status():
    unhealthy, errors = get_status()
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Super Platform Status\n")
        if unhealthy:
            f.write(f"Unhealthy containers: {', '.join(unhealthy)}\n")
        else:
            f.write("All containers healthy.\n")
        if errors:
            f.write("Recent errors:\n")
            for line in errors:
                f.write(line)
        else:
            f.write("No recent errors.\n")

if __name__ == "__main__":
    while True:
        write_status()
        time.sleep(300)  # Update every 5 minutes
