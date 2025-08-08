#!/usr/bin/env python3
"""
PERFECT MONITOR SCRIPT - Ensures 24/7 Operation WITHOUT Any Pauses
Watches your agent and shows live status dashboard
"""

import os
import sys
import time
import json
import sqlite3
import psutil
import subprocess
from datetime import datetime
from pathlib import Path
import threading

# Configuration
BASE_PATH = "Z:\\DiachronicValencyCorpus"
AGENT_SCRIPT = "final_complete_agent.py"
MONITOR_LOG = f"{BASE_PATH}\\monitor.log"

class PerfectMonitor:
    """
    Monitors the agent and ensures it NEVER stops
    Shows live dashboard of progress
    """
    
    def __init__(self):
        self.base_path = BASE_PATH
        self.running = True
        self.agent_pid = None
        self.start_time = datetime.now()
        
        # Statistics
        self.stats = {
            'agent_restarts': 0,
            'texts_downloaded': 0,
            'errors_handled': 0,
            'last_activity': datetime.now(),
            'uptime_hours': 0
        }
        
        # Ensure directories exist
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(f"{self.base_path}\\monitor_logs", exist_ok=True)
        
    def find_agent_process(self):
        """Find the agent Python process"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if any(AGENT_SCRIPT in str(cmd) for cmd in cmdline):
                        return proc.info['pid']
            except:
                pass
        return None
        
    def start_agent(self):
        """Start the agent if not running"""
        if not self.find_agent_process():
            print(f"\n🚀 Starting agent at {datetime.now().strftime('%H:%M:%S')}")
            
            # Start in a new process
            agent_path = os.path.join(self.base_path, AGENT_SCRIPT)
            if os.path.exists(agent_path):
                subprocess.Popen(
                    [sys.executable, agent_path],
                    cwd=self.base_path,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                self.stats['agent_restarts'] += 1
                time.sleep(5)  # Give it time to start
            else:
                print(f"⚠️  Agent script not found: {agent_path}")
                
    def check_agent_health(self):
        """Check if agent is healthy"""
        # Check process
        pid = self.find_agent_process()
        if not pid:
            return False
            
        # Check recent activity
        try:
            # Check if status file was updated recently
            status_file = f"{self.base_path}\\agent_status.json"
            if os.path.exists(status_file):
                mtime = datetime.fromtimestamp(os.path.getmtime(status_file))
                if (datetime.now() - mtime).seconds > 300:  # 5 minutes
                    return False
                    
            return True
        except:
            return False
            
    def update_statistics(self):
        """Update statistics from agent database"""
        try:
            # Try multiple database names
            db_files = [
                'corpus_complete.db',
                'corpus.db', 
                'consolidated_corpus.db',
                'safe_corpus.db'
            ]
            
            for db_file in db_files:
                db_path = f"{self.base_path}\\{db_file}"
                if os.path.exists(db_path):
                    db = sqlite3.connect(db_path)
                    cursor = db.cursor()
                    
                    # Get text count
                    try:
                        cursor.execute('SELECT COUNT(*) FROM texts')
                        self.stats['texts_downloaded'] = cursor.fetchone()[0]
                    except:
                        pass
                        
                    db.close()
                    break
                    
            # Update uptime
            uptime = datetime.now() - self.start_time
            self.stats['uptime_hours'] = uptime.total_seconds() / 3600
            
        except Exception as e:
            pass
            
    def show_live_dashboard(self):
        """Show live status dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print("🛡️  PERFECT MONITOR - 24/7 CORPUS COLLECTION")
        print("=" * 70)
        print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🚀 Uptime: {self.stats['uptime_hours']:.1f} hours")
        print("-" * 70)
        
        # Agent status
        agent_running = self.find_agent_process() is not None
        status_color = "🟢" if agent_running else "🔴"
        print(f"{status_color} Agent Status: {'RUNNING' if agent_running else 'STOPPED'}")
        
        if agent_running:
            print(f"   Process ID: {self.find_agent_process()}")
            
        # Statistics
        print(f"\n📊 COLLECTION STATISTICS:")
        print(f"   Texts Downloaded: {self.stats['texts_downloaded']}")
        print(f"   Agent Restarts: {self.stats['agent_restarts']}")
        print(f"   Last Activity: {self.stats['last_activity'].strftime('%H:%M:%S')}")
        
        # Disk space
        try:
            disk = psutil.disk_usage(self.base_path[0] + ':\\')
            print(f"\n💾 DISK SPACE:")
            print(f"   Used: {disk.used / (1024**3):.1f} GB")
            print(f"   Free: {disk.free / (1024**3):.1f} GB")
            print(f"   Percent: {disk.percent:.1f}%")
        except:
            pass
            
        # Current files
        try:
            text_dir = f"{self.base_path}\\texts\\collected"
            if os.path.exists(text_dir):
                files = list(Path(text_dir).glob('*.txt'))
                print(f"\n📚 RECENT DOWNLOADS:")
                for file in sorted(files, key=os.path.getmtime)[-5:]:
                    size_mb = file.stat().st_size / (1024**2)
                    print(f"   {file.name}: {size_mb:.1f} MB")
        except:
            pass
            
        # Health check
        print(f"\n🏥 HEALTH CHECK:")
        checks = {
            'Agent Process': agent_running,
            'Database Access': os.path.exists(f"{self.base_path}\\corpus_complete.db"),
            'Text Directory': os.path.exists(f"{self.base_path}\\texts\\collected"),
            'Free Disk Space': psutil.disk_usage(self.base_path[0] + ':\\').percent < 90
        }
        
        for check, status in checks.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {check}")
            
        print("\n" + "=" * 70)
        print("Press Ctrl+C to stop monitoring (agent will continue running)")
        
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Update statistics
                self.update_statistics()
                
                # Check agent health
                if not self.check_agent_health():
                    print(f"\n⚠️  Agent not healthy - restarting...")
                    self.start_agent()
                    
                # Show dashboard
                self.show_live_dashboard()
                
                # Save monitor status
                monitor_status = {
                    'timestamp': datetime.now().isoformat(),
                    'agent_running': self.find_agent_process() is not None,
                    'stats': self.stats
                }
                
                with open(f"{self.base_path}\\monitor_status.json", 'w') as f:
                    json.dump(monitor_status, f, indent=2)
                    
                # Wait before next check
                time.sleep(30)  # Update every 30 seconds
                
            except KeyboardInterrupt:
                print("\n\n🛑 Monitor stopping (agent continues running)")
                self.running = False
                break
            except Exception as e:
                print(f"\nMonitor error: {e}")
                time.sleep(60)
                
    def run(self):
        """Start monitoring"""
        print("🛡️  PERFECT MONITOR STARTING")
        print("This ensures your agent runs 24/7 without ANY pauses")
        print("-" * 70)
        
        # Ensure agent is running
        self.start_agent()
        
        # Start monitoring
        self.monitor_loop()
        

if __name__ == "__main__":
    monitor = PerfectMonitor()
    monitor.run()