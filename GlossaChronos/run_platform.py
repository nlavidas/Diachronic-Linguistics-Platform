import subprocess
import time
import webbrowser
from pathlib import Path
import sys
import os

class GlossaChronosPlatform:
    def __init__(self):
        self.services = []
        self.base_path = Path("Z:/")
        
    def start_service(self, name, command, cwd, env=None):
        """Start a service as subprocess"""
        print(f"Starting {name}...")
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env or os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        self.services.append((name, process))
        time.sleep(2)
        return process
    
    def start_all(self):
        # 1. Start NLP Server
        self.start_service(
            "NLP Server",
            [sys.executable, "server.py"],
            "Z:/NLPServer"
        )
        
        # 2. Start Bridge (UPDATED LINE HERE)
        self.start_service(
            "Bridge",
            [sys.executable, "stable_bridge.py"],  # Changed to stable_bridge.py
            "Z:/GlossaChronos"  # Changed directory
        )
        
        # 3. Start Ollama
        env = os.environ.copy()
        env["OLLAMA_MODELS"] = "Z:/OllamaModels/models"
        self.start_service(
            "Ollama",
            ["C:/Users/nlavi/AppData/Local/Programs/Ollama/ollama.exe", "serve"],
            "Z:/",
            env
        )
        
        # 4. Open control panel
        time.sleep(3)
        webbrowser.open("file:///Z:/Diachronic-Linguistics-Platform/glossachronos_control.html")
        
        print("\nAll services started! Press Ctrl+C to stop all.")
        
    def stop_all(self):
        for name, process in self.services:
            print(f"Stopping {name}...")
            process.terminate()

if __name__ == "__main__":
    platform = GlossaChronosPlatform()
    try:
        platform.start_all()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        platform.stop_all()