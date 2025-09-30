import os
import re
from pathlib import Path

class PPCHiGParser:
    def __init__(self):
        self.psd_path = 'Z:\\GlossaChronos\\PPCHiG'
        
    def list_psd_files(self):
        files = []
        for root, dirs, filenames in os.walk(self.psd_path):
            for f in filenames:
                if f.endswith('.psd'):
                    files.append(os.path.join(root, f))
        return files
    
    def parse_psd(self, filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Basic Penn Treebank parsing
        sentences = re.findall(r'\(.*?\)', content, re.DOTALL)
        return sentences[:5]  # First 5 sentences for testing
        
# Test
parser = PPCHiGParser()
files = parser.list_psd_files()
print(f"Found {len(files)} PSD files")
if files:
    print(f"Parsing first file: {files[0]}")
    sents = parser.parse_psd(files[0])
    print(f"Found {len(sents)} sentences")
