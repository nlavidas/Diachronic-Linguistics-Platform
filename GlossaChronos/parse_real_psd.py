import re

class PPCHiGActualParser:
    def __init__(self):
        self.psd_path = 'Z:\\GlossaChronos\\PPCHiG\\PSD'
        
    def parse_mark(self):
        with open(f'{self.psd_path}\\Mark.psd', 'r', encoding='utf-8') as f:
            content = f.read(5000)
        
        # Extract transliterated Greek words
        words = re.findall(r'[ÎîÏï][a-zA-ZÀ-ÿ]+', content)
        print(f"Greek words (transliterated): {words[:10]}")
        
        # Extract POS tags
        pos = re.findall(r'\(([A-Z\-]+)\s', content)
        print(f"POS tags: {pos[:10]}")
        
        # Extract verse references
        verses = re.findall(r'Mark:\d+_\d+', content)
        print(f"Verses: {verses[:5]}")
        
        return {'words': words[:20], 'pos': pos[:20]}

parser = PPCHiGActualParser()
result = parser.parse_mark()
