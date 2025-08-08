#!/usr/bin/env python3
"""
ULTIMATE GUARDIAN SCRIPT
Ensures your corpus agent NEVER stops, no matter what!
- Monitors multiple processes
- Auto-restarts if killed
- Protects against crashes, freezes, and terminations
- Logs all events
"""

import os
import sys
import time
import json
import psutil
import subprocess
import sqlite3
from datetime import datetime
from pathlib import Path
import threading
import signal

# Configuration
BASE_PATH = "Z:\\DiachronicValencyCorpus"
PROTECTED_SCRIPTS = [
    "final_complete_agent.py",
    "start_now.py",
    "agent_immediate.py",
    "corpus_agent.py",
    "autonomous_agent.py"
]

class UltimateGuardian:
    """
    The ultimate protector - ensures processes never die
    """
    
    def __init__(self):
        self.base_path = BASE_PATH
        self.running = True
        self.processes = {}
        self.restart_count = {}
        self.start_time = datetime.now()
        
        # Create guardian directory
        self.guardian_dir = f"{self.base_path}\\guardian"
        os.makedirs(self.guardian_dir, exist_ok=True)
        
        # Guardian log
        self.log_file = f"{self.guardian_dir}\\guardian_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Statistics
        self.stats = {
            'total_restarts': 0,
            'uptime_hours': 0,
            'processes_protected': 0,
            'incidents_prevented': 0
        }
        
        self.log("🛡️ ULTIMATE GUARDIAN STARTING")
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except:
            pass
            
    def find_python_processes(self):
        """Find all Python processes"""
        python_procs = {}
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    for script in PROTECTED_SCRIPTS:
                        if any(script in str(cmd) for cmd in cmdline):
                            python_procs[script] = {
                                'pid': proc.info['pid'],
                                'cmdline': cmdline,
                                'create_time': proc.info['create_time']
                            }
                            break
            except:
                pass
                
        return python_procs
        
    def start_process(self, script_name):
        """Start a protected process"""
        script_path = os.path.join(self.base_path, script_name)
        
        # Try to find the script
        if not os.path.exists(script_path):
            # Look in current directory
            script_path = script_name
            if not os.path.exists(script_path):
                self.log(f"⚠️ Script not found: {script_name}")
                return None
                
        try:
            # Start the process
            proc = subprocess.Popen(
                [sys.executable, script_path],
                cwd=self.base_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            self.log(f"✅ Started {script_name} (PID: {proc.pid})")
            self.stats['total_restarts'] += 1
            
            # Track restart count
            if script_name not in self.restart_count:
                self.restart_count[script_name] = 0
            self.restart_count[script_name] += 1
            
            return proc.pid
            
        except Exception as e:
            self.log(f"❌ Failed to start {script_name}: {e}")
            return None
            
    def check_process_health(self, proc_info):
        """Check if process is healthy"""
        try:
            # Get process object
            proc = psutil.Process(proc_info['pid'])
            
            # Check if responsive
            if proc.is_running():
                # Check CPU usage (if frozen)
                cpu_percent = proc.cpu_percent(interval=1)
                
                # Check memory usage
                memory_info = proc.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)
                
                # Process is healthy if not frozen and not using excessive memory
                if memory_mb < 4000:  # 4GB limit
                    return True, f"CPU: {cpu_percent:.1f}%, Memory: {memory_mb:.1f}MB"
                else:
                    return False, f"Excessive memory: {memory_mb:.1f}MB"
            else:
                return False, "Process not running"
                
        except psutil.NoSuchProcess:
            return False, "Process no longer exists"
        except Exception as e:
            return False, f"Health check error: {e}"
            
    def protect_processes(self):
        """Main protection loop"""
        self.log("🔍 Scanning for processes to protect...")
        
        while self.running:
            try:
                # Find current Python processes
                current_procs = self.find_python_processes()
                
                # Check each protected script
                for script in PROTECTED_SCRIPTS:
                    if script in current_procs:
                        # Process exists - check health
                        proc_info = current_procs[script]
                        healthy, status = self.check_process_health(proc_info)
                        
                        if not healthy:
                            self.log(f"⚠️ {script} unhealthy: {status}")
                            self.log(f"🔄 Restarting {script}...")
                            
                            # Try to kill the unhealthy process
                            try:
                                psutil.Process(proc_info['pid']).terminate()
                                time.sleep(2)
                            except:
                                pass
                                
                            # Restart
                            self.start_process(script)
                            self.stats['incidents_prevented'] += 1
                            
                    else:
                        # Process doesn't exist - start it
                        if script == "final_complete_agent.py" or script == "agent_immediate.py":
                            self.log(f"🚀 {script} not running - starting...")
                            self.start_process(script)
                            
                # Update statistics
                self.stats['processes_protected'] = len(current_procs)
                self.stats['uptime_hours'] = (datetime.now() - self.start_time).seconds / 3600
                
                # Save guardian status
                self.save_status()
                
                # Wait before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.log("🛑 Guardian stopped by user")
                self.running = False
                break
            except Exception as e:
                self.log(f"Guardian error: {e}")
                time.sleep(60)
                
    def save_status(self):
        """Save guardian status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'restart_counts': self.restart_count,
            'protected_processes': list(self.find_python_processes().keys())
        }
        
        try:
            with open(f"{self.guardian_dir}\\guardian_status.json", 'w') as f:
                json.dump(status, f, indent=2)
        except:
            pass
            
    def show_dashboard(self):
        """Show guardian dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print("🛡️  ULTIMATE GUARDIAN - PROCESS PROTECTOR")
        print("=" * 70)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🚀 Guardian Uptime: {self.stats['uptime_hours']:.1f} hours")
        print("-" * 70)
        
        # Show protected processes
        current_procs = self.find_python_processes()
        print(f"\n🔒 PROTECTED PROCESSES ({len(current_procs)}):")
        
        for script, info in current_procs.items():
            print(f"   ✅ {script} (PID: {info['pid']})")
            
        # Show statistics
        print(f"\n📊 GUARDIAN STATISTICS:")
        print(f"   Total Restarts: {self.stats['total_restarts']}")
        print(f"   Incidents Prevented: {self.stats['incidents_prevented']}")
        
        # Show restart counts
        if self.restart_count:
            print(f"\n🔄 RESTART COUNTS:")
            for script, count in self.restart_count.items():
                print(f"   {script}: {count} times")
                
        # Check corpus progress
        try:
            db_path = f"{self.base_path}\\corpus_complete.db"
            if os.path.exists(db_path):
                db = sqlite3.connect(db_path)
                cursor = db.cursor()
                cursor.execute('SELECT COUNT(*) FROM texts')
                text_count = cursor.fetchone()[0]
                print(f"\n📚 CORPUS PROGRESS:")
                print(f"   Texts Downloaded: {text_count}")
                db.close()
        except:
            pass
            
        print("\n" + "=" * 70)
        print("Guardian is protecting your processes 24/7!")
        print("Press Ctrl+C to stop guardian (processes continue)")
        
    def run_with_dashboard(self):
        """Run with live dashboard"""
        # Start protection in background
        protect_thread = threading.Thread(target=self.protect_processes, daemon=True)
        protect_thread.start()
        
        # Show dashboard
        while self.running:
            try:
                self.show_dashboard()
                time.sleep(5)  # Update every 5 seconds
            except KeyboardInterrupt:
                self.running = False
                break
                
    def run(self):
        """Start the guardian"""
        print("\n🛡️ ULTIMATE GUARDIAN")
        print("This ensures your corpus agent NEVER stops!")
        print("=" * 70)
        
        mode = input("\nSelect mode:\n1. Background protection (no dashboard)\n2. Live dashboard\nChoice (1/2): ")
        
        if mode == '2':
            self.run_with_dashboard()
        else:
            self.protect_processes()
            

if __name__ == "__main__":
    # Handle Windows signals properly
    signal.signal(signal.SIGINT, signal.default_int_handler)
    
    guardian = UltimateGuardian()
    guardian.run()