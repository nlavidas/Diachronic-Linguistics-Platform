#!/usr/bin/env python3
"""
FILE CONTENT VERIFICATION
Checks if file names match their actual content
"""

from pathlib import Path
import re

def verify_file_content(base_path="Z:\\DiachronicValencyCorpus"):
    """Check if file names match their content"""
    
    mismatches = []
    correct = []
    
    # Check preprocessed files
    preprocessed_path = Path(base_path) / "texts" / "preprocessed"
    
    for file_path in preprocessed_path.glob("*_CLEAN.txt"):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)  # Read first 2000 chars
            
        filename = file_path.stem.lower()
        
        # Extract work name from filename
        if 'aesop' in filename:
            expected_work = 'aesop|fables'
        elif 'aeneid' in filename:
            expected_work = 'aeneid|virgil|aeneas'
        elif 'iliad' in filename:
            expected_work = 'iliad|homer|achilles'
        elif 'odyssey' in filename:
            expected_work = 'odyssey|homer|odysseus'
        else:
            expected_work = filename.split('_')[0]
            
        # Check if content matches filename
        if not re.search(expected_work, content.lower()):
            # This is a mismatch!
            actual_work = 'Unknown'
            
            # Try to identify actual content
            if re.search(r'aeneid|virgil|aeneas', content.lower()):
                actual_work = 'Aeneid'
            elif re.search(r'iliad|achilles|troy', content.lower()):
                actual_work = 'Iliad'
            elif re.search(r'fables|aesop|moral', content.lower()):
                actual_work = 'Aesop Fables'
                
            mismatches.append({
                'file': file_path.name,
                'expected': filename,
                'actual': actual_work,
                'sample': content[:200]
            })
        else:
            correct.append(file_path.name)
            
    # Report findings
    print("="*60)
    print("FILE CONTENT VERIFICATION REPORT")
    print("="*60)
    
    if mismatches:
        print(f"\n❌ MISMATCHED FILES: {len(mismatches)}")
        for m in mismatches:
            print(f"\nFile: {m['file']}")
            print(f"Expected: {m['expected']}")
            print(f"Actually contains: {m['actual']}")
            print(f"Sample: {m['sample'][:100]}...")
            
            # Suggest fix
            new_name = m['file'].replace(m['expected'].split('_')[0], m['actual'].replace(' ', '_'))
            print(f"Suggested rename: {new_name}")
    else:
        print("\n✅ All files match their content!")
        
    print(f"\n✅ Correct files: {len(correct)}")
    
    return mismatches

if __name__ == "__main__":
    mismatches = verify_file_content()
    
    if mismatches:
        print("\n🔧 To fix mismatches, run:")
        print("python fix_file_mismatches.py")