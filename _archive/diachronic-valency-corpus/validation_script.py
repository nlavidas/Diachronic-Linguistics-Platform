#!/usr/bin/env python3
"""
VALIDATION & TESTING SCRIPT
Ensures everything works perfectly before starting
"""

import os
import sys
import sqlite3
import requests
import json
from datetime import datetime
from pathlib import Path

print("""
╔════════════════════════════════════════════════════════╗
║     DIACHRONIC CORPUS VALIDATION SCRIPT                ║
║     Checking all systems before launch...              ║
╚════════════════════════════════════════════════════════╝
""")

# Configuration
BASE_PATH = "Z:\\DiachronicValencyCorpus"
REQUIRED_DIRS = [
    'texts/collected',
    'texts/processed', 
    'valency/patterns',
    'logs',
    'ai_discoveries',
    'open_source_tools'
]

# Test results
tests_passed = 0
tests_failed = 0

def test_directory_structure():
    """Check if all required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    for dir_path in REQUIRED_DIRS:
        full_path = Path(BASE_PATH) / dir_path
        if full_path.exists():
            print(f"  ✅ {dir_path}")
            global tests_passed
            tests_passed += 1
        else:
            print(f"  ❌ {dir_path} - Creating...")
            full_path.mkdir(parents=True, exist_ok=True)
            global tests_failed
            tests_failed += 1

def test_database():
    """Test database connection and schema"""
    print("\n🔍 Testing database...")
    
    try:
        db_path = Path(BASE_PATH) / 'corpus_complete.db'
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        required_tables = ['texts', 'valency_patterns', 'translation_chains', 'consultations']
        
        for table in required_tables:
            if (table,) in tables:
                print(f"  ✅ Table '{table}' exists")
                global tests_passed
                tests_passed += 1
            else:
                print(f"  ❌ Table '{table}' missing")
                global tests_failed
                tests_failed += 1
                
        conn.close()
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        tests_failed += 1

def test_internet_connection():
    """Test internet connectivity"""
    print("\n🔍 Testing internet connection...")
    
    test_urls = [
        ('Project Gutenberg', 'https://www.gutenberg.org'),
        ('Perseus Digital Library', 'https://www.perseus.tufts.edu'),
        ('Internet Archive', 'https://archive.org')
    ]
    
    for name, url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {name} accessible")
                global tests_passed
                tests_passed += 1
            else:
                print(f"  ⚠️  {name} returned status {response.status_code}")
                global tests_failed
                tests_failed += 1
        except Exception as e:
            print(f"  ❌ {name} unreachable: {e}")
            tests_failed += 1

def test_python_dependencies():
    """Test required Python packages"""
    print("\n🔍 Testing Python dependencies...")
    
    packages = [
        'requests',
        'sqlite3',
        'json',
        'logging',
        'threading',
        'schedule'
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
            global tests_passed
            tests_passed += 1
        except ImportError:
            print(f"  ❌ {package} not installed")
            global tests_failed
            tests_failed += 1

def test_sample_download():
    """Test downloading a small file"""
    print("\n🔍 Testing download capability...")
    
    try:
        # Test with a small Gutenberg text
        test_url = 'https://www.gutenberg.org/files/1/1-0.txt'
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200 and len(response.text) > 100:
            print(f"  ✅ Download test successful ({len(response.text)} bytes)")
            global tests_passed
            tests_passed += 1
        else:
            print(f"  ❌ Download test failed")
            global tests_failed
            tests_failed += 1
            
    except Exception as e:
        print(f"  ❌ Download error: {e}")
        tests_failed += 1

def main():
    """Run all validation tests"""
    print(f"\nStarting validation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Run tests
    test_directory_structure()
    test_database()
    test_internet_connection()
    test_python_dependencies()
    test_sample_download()
    
    # Summary
    print("\n" + "="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60)
    print(f"✅ Tests passed: {tests_passed}")
    print(f"❌ Tests failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ready to start the agent!")
        print("\nNext step: python ultimate_24_7_agent_with_ai.py")
        return True
    else:
        print("\n⚠️  Some tests failed. Please fix issues before starting.")
        print("The agent may still work, but some features might be limited.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)