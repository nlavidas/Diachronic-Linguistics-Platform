import logging
from pathlib import Path
import sys
import time
import subprocess

# --- SETUP ---
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# (We will add our action functions here from agent_actions.py later)

class UltimateCorpusController:
    def __init__(self):
        self.project_root = project_root
        self.db_path = self.project_root / "corpus.db"
        
    def status_report(self):
        print("\n--- 📊 CORPUS STATUS REPORT ---")
        # In the future, this will connect to our Streamlit dashboard
        print("Status: All systems nominal. Preprocessor agent is idle.")
        print(f"Database size: {self.db_path.stat().st_size / 1_000_000:.2f} MB")

    def run_full_pipeline(self):
        print("\n🚀 Starting Full Pipeline (Harvest & Process)...")
        # This is a placeholder for running our full 24/7 agent logic
        # We will add the code to call the harvest/process missions here
        time.sleep(10)
        print("✅ Full Pipeline mission complete.")
        
    def interactive_menu(self):
        """The main control menu for the entire ecosystem."""
        while True:
            print("\n" + "="*40)
            print("🎮 ULTIMATE CORPUS CONTROLLER 🎮")
            print("="*40)
            print("1. 📊 Status Report")
            print("2. 🚀 Run Full Weekend Pipeline (Harvest & Process)")
            print("3. 🛰️ Launch Monitoring Dashboard")
            print("4. 🐙 Sync Project to GitHub")
            print("0. ❌ Exit")
            print("="*40)
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.status_report()
            elif choice == '2':
                self.run_full_pipeline()
            elif choice == '3':
                print("Launching Streamlit Dashboard in new window...")
                subprocess.Popen(f'powershell -Command "cd {self.project_root}; .\\venv\\Scripts\\Activate.ps1; streamlit run scripts/01_Home.py --server.port 8502"', shell=True)
            elif choice == '4':
                print("Syncing to GitHub...")
                # (We will add the git sync logic here)
            elif choice == '0':
                print("👋 Goodbye!"); break
            else:
                print("❌ Invalid choice.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    controller = UltimateCorpusController()
    controller.interactive_menu()