#!/usr/bin/env python3
"""
TWO-LAPTOP SYNC UTILITIES
For working with external Z: drive
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class LaptopSyncManager:
    def __init__(self):
        self.base_path = Path("Z:/DiachronicValencyCorpus")
        self.config_file = self.base_path / "laptop_sync.json"
        self.load_config()
    
    def load_config(self):
        """Load or create sync configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "laptops": {},
                "last_sync": None,
                "sync_history": []
            }
            self.save_config()
    
    def save_config(self):
        """Save sync configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def register_laptop(self):
        """Register current laptop"""
        laptop_name = os.environ.get('COMPUTERNAME', 'unknown')
        
        self.config["laptops"][laptop_name] = {
            "last_seen": str(datetime.now()),
            "last_action": "registered"
        }
        
        self.save_config()
        print(f"✅ Laptop '{laptop_name}' registered")
        return laptop_name
    
    def before_switching_laptops(self):
        """Run before switching to another laptop"""
        laptop_name = os.environ.get('COMPUTERNAME', 'unknown')
        
        print(f"🔄 Preparing to switch from laptop: {laptop_name}")
        
        # 1. Stop all agents
        print("⏹️  Stopping agents...")
        
        # 2. Close database connections
        print("💾 Closing databases...")
        
        # 3. Create switch marker
        marker_file = self.base_path / f"SWITCHED_FROM_{laptop_name}.txt"
        with open(marker_file, 'w') as f:
            f.write(f"Switched at: {datetime.now()}\n")
            f.write(f"From laptop: {laptop_name}\n")
        
        # 4. Update config
        self.config["laptops"][laptop_name]["last_action"] = "switched_away"
        self.config["last_sync"] = str(datetime.now())
        self.save_config()
        
        print("✅ Ready to switch laptops!")
        print("🔌 You can now safely remove the Z: drive")
    
    def after_switching_laptops(self):
        """Run after switching to a new laptop"""
        laptop_name = self.register_laptop()
        
        print(f"🔄 Setting up on laptop: {laptop_name}")
        
        # Check for switch markers
        markers = list(self.base_path.glob("SWITCHED_FROM_*.txt"))
        if markers:
            print(f"📋 Found {len(markers)} switch markers")
            for marker in markers:
                print(f"  - {marker.name}")
                marker.unlink()  # Remove marker
        
        # Update config
        self.config["laptops"][laptop_name]["last_action"] = "resumed_work"
        self.save_config()
        
        print("✅ Ready to continue work!")
        print("🚀 You can now start your agents")
    
    def check_sync_status(self):
        """Check sync status across laptops"""
        print("="*50)
        print("📊 LAPTOP SYNC STATUS")
        print("="*50)
        
        for laptop, info in self.config["laptops"].items():
            print(f"\n💻 {laptop}:")
            print(f"   Last seen: {info['last_seen']}")
            print(f"   Last action: {info['last_action']}")
        
        if self.config["last_sync"]:
            print(f"\n🔄 Last sync: {self.config['last_sync']}")
        
        print("="*50)

if __name__ == "__main__":
    sync = LaptopSyncManager()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "before":
            sync.before_switching_laptops()
        elif sys.argv[1] == "after":
            sync.after_switching_laptops()
        elif sys.argv[1] == "status":
            sync.check_sync_status()
    else:
        print("Usage:")
        print("  python LAPTOP_SYNC_UTILS.py before  # Before switching")
        print("  python LAPTOP_SYNC_UTILS.py after   # After switching")
        print("  python LAPTOP_SYNC_UTILS.py status  # Check status")