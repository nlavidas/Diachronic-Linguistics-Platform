import os
import re

class PPCHiGRealParser:
    def __init__(self):
        self.psd_path = 'Z:\\GlossaChronos\\PPCHiG\\PSD'
        
    def inspect_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000)  # First 1000 chars
        
        # Look for any patterns
        print("File sample:", content[:500])
        
        # Check for transliterated Greek
        words = re.findall(r'\b[a-zA-Z]+\b', content)
        print(f"Found {len(words)} words")
        print("Sample words:", words[:20])
        
        # Check structure markers
        brackets = content.count('(')
        print(f"Found {brackets} opening brackets")
        
# Inspect Mark.psd
parser = PPCHiGRealParser()
parser.inspect_file('Z:\\GlossaChronos\\PPCHiG\\PSD\\Mark.psd')
