"""
API Configuration Manager
Handles secure API key input and storage
"""
import os
import json
import getpass
from pathlib import Path

class APIConfigManager:
    def __init__(self):
        self.config_file = Path.home() / '.diachronic_corpus' / 'api_keys.json'
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.apis = {}
        
    def load_saved_keys(self):
        """Load previously saved API keys"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.apis = json.load(f)
                return True
            except:
                return False
        return False
    
    def save_keys(self):
        """Save API keys securely to user home directory"""
        with open(self.config_file, 'w') as f:
            json.dump(self.apis, f)
        # Set file permissions to be readable only by user
        if os.name != 'nt':  # Unix-like systems
            os.chmod(self.config_file, 0o600)
    
    def get_api_key(self, service_name, description="", required=True):
        """Get API key for a service, prompting if needed"""
        # First check environment variable
        env_var = f"{service_name.upper()}_API_KEY"
        if os.getenv(env_var):
            return os.getenv(env_var)
        
        # Check saved keys
        if service_name in self.apis and self.apis[service_name]:
            return self.apis[service_name]
        
        # If not required, return None
        if not required:
            return None
            
        # Prompt user
        print(f"\n{'='*60}")
        print(f"API Key Required: {service_name}")
        if description:
            print(f"Description: {description}")
        print(f"{'='*60}")
        
        while True:
            print(f"\nOptions for {service_name}:")
            print("1. Enter API key now")
            print("2. Skip (some features may not work)")
            print("3. Get help on obtaining this API key")
            
            choice = input("\nYour choice (1-3): ").strip()
            
            if choice == '1':
                key = input(f"Enter {service_name} API key: ").strip()
                if key:
                    self.apis[service_name] = key
                    save_choice = input("Save this key for future sessions? (y/n): ").lower()
                    if save_choice == 'y':
                        self.save_keys()
                        print("✓ Key saved securely")
                    return key
                else:
                    print("! No key entered")
                    
            elif choice == '2':
                print(f"⚠ Skipping {service_name} - some features may not work")
                return None
                
            elif choice == '3':
                self.show_api_help(service_name)
                
    def show_api_help(self, service_name):
        """Show help for obtaining API keys"""
        help_info = {
            'anthropic': """
To get an Anthropic API key:
1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to 'API Keys'
4. Click 'Create Key'
5. Copy the key (starts with 'sk-')
Note: You need a paid account for API access
""",
            'openai': """
To get an OpenAI API key:
1. Go to: https://platform.openai.com/
2. Sign up or log in  
3. Navigate to 'API keys'
4. Click 'Create new secret key'
5. Copy the key (starts with 'sk-')
""",
            'weblicht': """
WebLicht API:
1. Go to: https://weblicht.sfs.uni-tuebingen.de/
2. Register for an account
3. Request API access
4. Your API key will be emailed to you
""",
            'diorisis': """
Diorisis API:
1. Visit: http://www.diorisis.org/
2. Contact them for API access
3. Academic affiliations may get free access
"""
        }
        
        if service_name.lower() in help_info:
            print(help_info[service_name.lower()])
        else:
            print(f"No specific help available for {service_name}")
            print("Check the service's documentation for API access")
    
    def clear_saved_keys(self):
        """Clear all saved API keys"""
        confirm = input("Are you sure you want to clear all saved API keys? (yes/no): ")
        if confirm.lower() == 'yes':
            self.apis = {}
            if self.config_file.exists():
                self.config_file.unlink()
            print("✓ All saved API keys cleared")
        else:
            print("Cancelled")

# Global instance
api_manager = APIConfigManager()

def get_configured_apis():
    """Get all required API keys for the corpus system"""
    print("\n" + "="*60)
    print("Diachronic Valency Corpus - API Configuration")
    print("="*60)
    
    # Load any previously saved keys
    if api_manager.load_saved_keys():
        print("✓ Found saved API keys")
        use_saved = input("Use saved API keys? (y/n/clear): ").lower()
        if use_saved == 'clear':
            api_manager.clear_saved_keys()
        elif use_saved != 'y':
            api_manager.apis = {}
    
    # Get required APIs
    apis = {
        'anthropic': api_manager.get_api_key(
            'anthropic',
            'For AI-powered text analysis and extraction',
            required=True
        ),
        'weblicht': api_manager.get_api_key(
            'weblicht', 
            'For linguistic annotation fallback',
            required=False
        ),
        'diorisis': api_manager.get_api_key(
            'diorisis',
            'For Ancient Greek text processing', 
            required=False
        )
    }
    
    print("\n" + "="*60)
    print("API Configuration Complete")
    print("✓ Required APIs configured:", sum(1 for v in apis.values() if v))
    print("="*60 + "\n")
    
    return apis

if __name__ == "__main__":
    # Test the configuration
    apis = get_configured_apis()
    print("Configured APIs:", {k: '***' if v else None for k, v in apis.items()})
