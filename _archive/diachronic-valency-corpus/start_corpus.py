#!/usr/bin/env python3
"""
Simple starter script for the Diachronic Valency Corpus
Handles API configuration and launches the orchestrator
"""
import os
import sys
import subprocess
from api_config_manager import api_manager, get_configured_apis

def check_requirements():
    """Check if basic requirements are met"""
    print("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        return False
    print("✓ Python version OK")
    
    # Check for PostgreSQL
    try:
        import psycopg2
        print("✓ PostgreSQL driver installed")
    except ImportError:
        print("❌ PostgreSQL driver not found")
        print("  Run: pip install psycopg2-binary")
        return False
    
    # Check if data directory exists
    os.makedirs("data/texts", exist_ok=True)
    print("✓ Data directory ready")
    
    return True

def show_menu():
    """Show main menu"""
    print("\n" + "="*60)
    print("Diachronic Valency Corpus - Main Menu")
    print("="*60)
    print("1. Start corpus collection (24/7 mode)")
    print("2. Process local files only")
    print("3. Configure API keys")
    print("4. Test database connection")
    print("5. View logs")
    print("6. Exit")
    print("="*60)
    
    return input("Select option (1-6): ").strip()

def test_database():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        import psycopg2
        dsn = os.getenv("DATABASE_URL", "dbname=corpus user=postgres password=postgres host=localhost port=5432")
        conn = psycopg2.connect(dsn)
        conn.close()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nMake sure PostgreSQL is running and the 'corpus' database exists")
        print("You can create it with: CREATE DATABASE corpus;")
        return False

def view_logs():
    """View recent log entries"""
    log_file = "master_orchestrator.log"
    if os.path.exists(log_file):
        print(f"\nLast 20 lines from {log_file}:")
        print("-" * 60)
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-20:]:
                print(line.rstrip())
    else:
        print("No log file found yet")

def main():
    """Main entry point"""
    print("\n🌟 Welcome to the Diachronic Valency Corpus System 🌟")
    
    if not check_requirements():
        print("\n❌ Please fix the requirements above and try again")
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            # Start full system
            print("\nConfiguring APIs for full system...")
            apis = get_configured_apis()
            
            if not apis.get('anthropic'):
                print("\n⚠ Warning: No Anthropic API key configured")
                print("Some AI features will not work")
                cont = input("Continue anyway? (y/n): ")
                if cont.lower() != 'y':
                    continue
            
            if test_database():
                print("\nStarting master orchestrator...")
                print("Press Ctrl+C to stop")
                try:
                    subprocess.run([sys.executable, "master_orchestrator.py"])
                except KeyboardInterrupt:
                    print("\n✓ Orchestrator stopped")
            
        elif choice == '2':
            # Process local files only
            print("\nStarting in local mode...")
            print("Place text files in: data/texts/")
            print("Press Ctrl+C to stop")
            # You can create a simpler version here
            
        elif choice == '3':
            # Configure APIs
            api_manager.apis = {}  # Clear current config
            apis = get_configured_apis()
            
        elif choice == '4':
            # Test database
            test_database()
            
        elif choice == '5':
            # View logs
            view_logs()
            
        elif choice == '6':
            # Exit
            print("\nGoodbye! 👋")
            break
        
        else:
            print("Invalid option, please try again")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
