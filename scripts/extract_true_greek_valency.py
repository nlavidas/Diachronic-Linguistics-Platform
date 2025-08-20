import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from scripts.improved_greek_morphology import ImprovedGreekMorphology

def extract_true_greek_valency():
   print('[INFO] --- Valency Extractor Initialized ---')
   morphology = ImprovedGreekMorphology()
   # Call the run method instead of analyze
   morphology.run()
   print('[INFO] --- Valency Extraction Complete ---')

if __name__ == '__main__':
   extract_true_greek_valency()
