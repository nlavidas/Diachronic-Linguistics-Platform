import logging
from pathlib import Path
import sys
import time
import subprocess

# --- SETUP ---
# Ensure the project root is on the Python path to find our other scripts
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Import the agent that will run in the background
from scripts.super_agent import main as run_super_agent

# --- The Main Controller Class (inspired by your script) ---
class UltimateCorpusController:
    def __init__(self):
        self.project_root = project_root
        self.db_path = self.project_root / "corpus.db"
        
    def status_report(self):
        """A simple status report, to be expanded later."""
        print("\n--- 📊 CORPUS STATUS REPORT ---")
        if self.db_path.exists():
            print(f"Database Size: {self.db_path.stat().st_size / 1_000_000:.2f} MB")
        else:
            print("Database has not been created yet.")
        print("Agent Status: Check other terminal windows for live agent logs.")

    def launch_platform(self):
        """Launches the Streamlit dashboard in a new window."""
        print("Launching Streamlit Dashboard...")
        # This command activates the venv and starts Streamlit
        command = f"cd '{self.project_root}'; .\\venv\\Scripts\\Activate.ps1; streamlit run scripts/01_Home.py --server.port 8502"
        subprocess.Popen(f'powershell -NoExit -Command "{command}"', shell=True)

    def interactive_menu(self):
        """The main control menu for the entire ecosystem."""
        while True:
            print("\n" + "="*40)
            print("      🎮 ECOSYSTEM CONTROL PANEL 🎮")
            print("="*40)
            print("1. 📊 Status Report")
            print("2. 🚀 Launch 24/7 Super Agent (in a new window)")
            print("3. 🛰️  Launch Monitoring Platform")
            print("4. 🐙 Sync Project to GitHub")
            print("0. ❌ Exit")
            print("="*40)
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.status_report()
            elif choice == '2':
                print("Launching Super Agent in a new window...")
                python_executable = str(self.project_root / "venv" / "Scripts" / "python.exe")
                agent_script = str(self.project_root / "scripts" / "super_agent.py")
                agent_command = f"cd '{self.project_root}'; .\\venv\\Scripts\\Activate.ps1; python '{agent_script}'; pause"
                subprocess.Popen(f'powershell -NoExit -Command "{agent_command}"', shell=True)
            elif choice == '3':
                self.launch_platform()
            elif choice == '4':
                print("Syncing to GitHub...")
                # Add git sync logic here in the future
            elif choice == '0':
                print("👋 Goodbye!"); break
            else:
                print("❌ Invalid choice.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    controller = UltimateCorpusController()
    controller.interactive_menu()