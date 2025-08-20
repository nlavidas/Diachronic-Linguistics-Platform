import sys
from pathlib import Path
import time

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

mission_file = project_root / "master_mission.txt"

print(f"Checking mission file: {mission_file}")
print(f"File exists: {mission_file.exists()}")

while True:
    if mission_file.exists():
        with open(mission_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            missions = [l.strip() for l in lines if l.strip() and not l.startswith('#')]
            
        if missions:
            print(f"\nFound {len(missions)} missions!")
            print(f"Next mission: {missions[0]}")
            
            # Remove first mission
            with open(mission_file, 'w', encoding='utf-8') as f:
                f.writelines(lines[1:])
            
            print(f"Processing: {missions[0]}")
            time.sleep(2)
        else:
            print(".", end="", flush=True)
            time.sleep(5)
    else:
        print("No mission file!")
        break
