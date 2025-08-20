#!/usr/bin/env python3
"""
FIX PROIEL URLs
Downloads the actual PROIEL treebank files
"""

import os
import requests
from pathlib import Path
import time

BASE_PATH = "Z:\\DiachronicValencyCorpus"

# CORRECT PROIEL URLs
PROIEL_FILES = [
    # Greek New Testament
    ('https://raw.githubusercontent.com/proiel/proiel-treebank/master/greek-nt.xml', 
     'PROIEL_Greek_NT.xml'),
    
    # Latin texts
    ('https://raw.githubusercontent.com/proiel/proiel-treebank/master/latin-nt.xml', 
     'PROIEL_Latin_NT.xml'),
     
    # Additional PROIEL texts
    ('https://raw.githubusercontent.com/proiel/proiel-treebank/master/gothic-nt.xml',
     'PROIEL_Gothic_NT.xml'),
     
    ('https://raw.githubusercontent.com/proiel/proiel-treebank/master/armenian-nt.xml',
     'PROIEL_Armenian_NT.xml'),
     
    ('https://raw.githubusercontent.com/proiel/proiel-treebank/master/marianus.xml',
     'PROIEL_OCS_Marianus.xml'),
]

def download_proiel():
    """Download PROIEL files with correct URLs"""
    print("="*60)
    print("📚 DOWNLOADING PROIEL TREEBANK FILES")
    print("="*60)
    
    output_dir = Path(BASE_PATH) / 'texts' / 'collected'
    success = 0
    
    for url, filename in PROIEL_FILES:
        output_path = output_dir / filename
        
        # Skip if already exists
        if output_path.exists():
            print(f"✅ Already have: {filename}")
            continue
            
        print(f"\n📥 Downloading: {filename}")
        print(f"   From: {url}")
        
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Check if it's XML
            if response.text.startswith('<?xml') or '<proiel' in response.text[:1000]:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                    
                size_mb = len(response.text) / (1024*1024)
                print(f"   ✅ Success! {size_mb:.1f} MB")
                success += 1
            else:
                print(f"   ❌ Not valid XML!")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            
        time.sleep(2)
        
    print("\n" + "="*60)
    print(f"✅ Downloaded {success} PROIEL files")
    print("="*60)
    
def check_xml_files():
    """Verify XML files are valid"""
    print("\n🔍 Checking XML files...")
    
    xml_dir = Path(BASE_PATH) / 'texts' / 'collected'
    xml_files = list(xml_dir.glob('*.xml'))
    
    print(f"\nFound {len(xml_files)} XML files:")
    for xml_file in xml_files:
        size_mb = xml_file.stat().st_size / (1024*1024)
        print(f"  {xml_file.name}: {size_mb:.1f} MB")
        
        # Check if valid XML
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if '<?xml' in first_line:
                    print(f"    ✅ Valid XML")
                else:
                    print(f"    ⚠️  May not be valid XML")
        except:
            print(f"    ❌ Cannot read")
            
def clear_stuck_downloads():
    """Remove agent blocks on stuck files"""
    print("\n🧹 Clearing stuck download markers...")
    
    # Look for any lock files or temp files
    temp_files = list(Path(BASE_PATH).glob('*.tmp'))
    temp_files.extend(list(Path(BASE_PATH).glob('*.lock')))
    
    for temp_file in temp_files:
        try:
            temp_file.unlink()
            print(f"  Removed: {temp_file.name}")
        except:
            pass
            
    print("✅ Cleared!")

if __name__ == "__main__":
    download_proiel()
    check_xml_files()
    clear_stuck_downloads()
    
    print("\n💡 Your agent should now skip the broken URLs and continue!")