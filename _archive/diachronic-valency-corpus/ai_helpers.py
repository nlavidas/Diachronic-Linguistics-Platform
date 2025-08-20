"""
Helper functions for AI model integration
"""
import os
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL

def setup_claude():
    """Set up Claude API environment variables"""
    os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
    os.environ["ANTHROPIC_MODEL"] = ANTHROPIC_MODEL
    print(f"Claude model set to: {ANTHROPIC_MODEL}")
    return True
