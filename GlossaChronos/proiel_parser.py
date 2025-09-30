import xml.etree.ElementTree as ET
from pathlib import Path

class PROIELParser:
    """Parse real PROIEL XML format"""
    
    def parse_proiel_file(self, xml_path):
        """Parse actual PROIEL treebank XML"""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        sentences = []
        for sentence in root.findall('.//sentence'):
            sent_data = {
                'id': sentence.get('id'),
                'tokens': []
            }
            
            for token in sentence.findall('.//token'):
                sent_data['tokens'].append({
                    'form': token.get('form'),
                    'lemma': token.get('lemma'),
                    'pos': token.get('part-of-speech'),
                    'morph': token.get('morphology'),
                    'head': token.get('head-id'),
                    'relation': token.get('relation')
                })
            
            sentences.append(sent_data)
        
        return sentences
    
    def generate_conllu(self, sentences):
        """Convert PROIEL to CoNLL-U format"""
        conllu_lines = []
        for sent in sentences:
            conllu_lines.append(f"# sent_id = {sent['id']}")
            for i, token in enumerate(sent['tokens'], 1):
                line = f"{i}\t{token['form']}\t{token['lemma']}\t_\t{token['pos']}\t{token['morph']}\t{token['head']}\t{token['relation']}\t_\t_"
                conllu_lines.append(line)
            conllu_lines.append("")
        
        return "\n".join(conllu_lines)