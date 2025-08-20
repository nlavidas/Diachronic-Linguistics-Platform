"""
Configuration for the Diachronic Valency Corpus
Contains API keys and model settings
"""
import os
from api_config_manager import api_manager


# Get API key from file, environment, or prompt
def get_anthropic_key():
    """Get Anthropic API key from api_key.txt, environment, or prompt user"""
    # 1. Try environment variable
    env_key = os.getenv("ANTHROPIC_API_KEY")
    if env_key:
        return env_key
    # 2. Try api_key.txt
    key_file = os.path.join(os.path.dirname(__file__), "api_key.txt")
    if os.path.exists(key_file):
        with open(key_file, "r", encoding="utf-8") as f:
            key = f.read().strip()
            if key:
                return key
    # 3. Prompt user
    print("\nPlease enter your Anthropic API key (will not be saved):")
    key = input("API key: ").strip()
    return key

# Anthropic API Configuration
ANTHROPIC_API_KEY = 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  # Will be set when needed
ANTHROPIC_MODEL = "claude-3-opus-20240229"  # Latest Claude 3 Opus model

# API Base URL
ANTHROPIC_API_BASE = "https://api.anthropic.com/v1"

# System settings
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# Initialize API key on import if needed
def init_api_keys():
    global ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        ANTHROPIC_API_KEY = get_anthropic_key()
    return ANTHROPIC_API_KEY
