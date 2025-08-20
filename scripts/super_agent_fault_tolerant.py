import logging
import time
import sys
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(project_root / "super_agent_fault_tolerant.log", mode='a')
    ]
)
logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "closed"
        
    def is_open(self):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
                return False
            return True
        return False
        
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")
            
    def record_success(self):
        if self.state == "half-open":
            logger.info("Circuit breaker closing after successful operation")
        self.failure_count = 0
        self.state = "closed"

class FaultTolerantSuperAgent:
    def __init__(self):
        self.is_running = True
        self.start_time = time.time()
        self.mission_count = 0
        self.error_count = 0
        self.circuit_breaker = CircuitBreaker()
        self.checkpoint_file = project_root / "agent_checkpoint.json"
        self.mission_queue_file = project_root / "master_mission.txt"
        self.db_path = project_root / "corpus.db"
        
        if not self.checkpoint_file.exists():
            self.create_checkpoint()
        self.load_checkpoint()
        
    def create_checkpoint(self):
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'mission_count': self.mission_count,
            'error_count': self.error_count,
            'uptime': time.time() - self.start_time
        }
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)
            logger.info(f"Checkpoint created: {self.mission_count} missions processed")
        except Exception as e:
            logger.error(f"Failed to create checkpoint: {e}")
            
    def load_checkpoint(self):
        try:
            if self.checkpoint_file.exists():
                with open(self.checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                    self.mission_count = checkpoint.get('mission_count', 0)
                    self.error_count = checkpoint.get('error_count', 0)
                    logger.info(f"Loaded checkpoint: {self.mission_count} missions previously processed")
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            
    def get_next_mission(self):
        if not self.mission_queue_file.exists():
            return None
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with open(self.mission_queue_file, 'r+', encoding='utf-8') as f:
                    lines = f.readlines()
                    if not lines:
                        return None
                        
                    next_mission = None
                    remaining_lines = []
                    
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if next_mission is None:
                                next_mission = line
                            else:
                                remaining_lines.append(line + '\n')
                        elif line:
                            remaining_lines.append(line + '\n')
                    
                    f.seek(0)
                    f.truncate()
                    f.writelines(remaining_lines)
                    
                    return next_mission
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed to get mission: {e}")
                time.sleep(1)
                
        return None
        
    def process_mission_with_retry(self, mission_string):
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                if self.circuit_breaker.is_open():
                    logger.warning("Circuit breaker open, skipping mission")
                    self.requeue_mission(mission_string)
                    return False
                    
                logger.info(f"Processing mission: {mission_string}")
                
                # Import and execute mission
                from scripts.agent_actions import setup_database, process_mission_action
                setup_database()
                process_mission_action(mission_string)
                
                self.circuit_breaker.record_success()
                self.mission_count += 1
                logger.info(f"Mission completed successfully: {mission_string}")
                return True
                
            except Exception as e:
                self.circuit_breaker.record_failure()
                self.error_count += 1
                
                if attempt == max_retries - 1:
                    logger.error(f"Mission failed after {max_retries} attempts: {e}")
                    self.write_to_error_log(mission_string, str(e))
                    return False
                    
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Mission failed, retry {attempt+1}/{max_retries} in {delay}s: {e}")
                time.sleep(delay)
                
        return False
        
    def requeue_mission(self, mission_string):
        try:
            with open(self.mission_queue_file, 'a', encoding='utf-8') as f:
                f.write(f"\n# Requeued at {datetime.now().isoformat()}\n")
                f.write(f"{mission_string}\n")
            logger.info(f"Mission requeued: {mission_string}")
        except Exception as e:
            logger.error(f"Failed to requeue mission: {e}")
            
    def write_to_error_log(self, mission, error):
        error_file = project_root / "failed_missions.log"
        try:
            with open(error_file, 'a', encoding='utf-8') as f:
                f.write(f"\n[{datetime.now().isoformat()}]\n")
                f.write(f"Mission: {mission}\n")
                f.write(f"Error: {error}\n")
                f.write("-" * 50 + "\n")
        except Exception as e:
            logger.error(f"Failed to write to error log: {e}")
            
    def health_check(self):
        health_status = {'healthy': True, 'issues': []}
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            conn.execute("SELECT 1")
            conn.close()
        except Exception as e:
            health_status['healthy'] = False
            health_status['issues'].append(f"Database issue: {e}")
            
        import shutil
        total, used, free = shutil.disk_usage("Z:\\")
        free_gb = free // (2**30)
        if free_gb < 1:
            health_status['healthy'] = False
            health_status['issues'].append(f"Low disk space: {free_gb}GB")
            
        if not health_status['healthy']:
            logger.warning(f"Health check failed: {health_status['issues']}")
            
        return health_status
        
    def run(self):
        logger.info(" Fault-Tolerant Super Agent Starting...")
        
        last_checkpoint_time = time.time()
        checkpoint_interval = 300
        last_health_check = time.time()
        health_check_interval = 60
        
        while self.is_running:
            try:
                self.last_heartbeat = time.time()
                
                if time.time() - last_health_check > health_check_interval:
                    health = self.health_check()
                    last_health_check = time.time()
                    
                    if not health['healthy']:
                        logger.warning("System unhealthy, waiting 30 seconds...")
                        time.sleep(30)
                        continue
                
                mission = self.get_next_mission()
                
                if mission:
                    success = self.process_mission_with_retry(mission)
                    
                    if success and time.time() - last_checkpoint_time > checkpoint_interval:
                        self.create_checkpoint()
                        last_checkpoint_time = time.time()
                else:
                    logger.info("No missions in queue. Waiting 60 seconds...")
                    time.sleep(60)
                    
            except KeyboardInterrupt:
                logger.info("Shutdown signal received")
                self.is_running = False
                break
                
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
                self.error_count += 1
                
                if self.error_count > 10:
                    logger.critical("Too many errors, pausing for 5 minutes")
                    time.sleep(300)
                    self.error_count = 0
                else:
                    time.sleep(10)
                    
        self.create_checkpoint()
        logger.info(f"Agent stopped. Processed {self.mission_count} missions with {self.error_count} errors")

def main():
    try:
        import psutil
    except ImportError:
        logger.info("Installing psutil for system monitoring...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
        
    agent = FaultTolerantSuperAgent()
    agent.run()

if __name__ == "__main__":
    main()
