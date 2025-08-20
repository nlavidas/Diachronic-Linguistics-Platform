#!/usr/bin/env python3
"""
PROIEL XML PREPROCESSOR
Handles PROIEL-style XML files and converts to annotated text format
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json
import logging

class PROIELPreprocessor:
    def __init__(self, base_path="Z:\\DiachronicValencyCorpus"):
        self.base_path = Path(base_path)
        self.xml_path = self.base_path / "texts" / "collected"
        self.output_path = self.base_path / "texts" / "proiel_processed"
        self.output_path.mkdir(exist_ok=True)
        
    def process_proiel_xml(self, xml_file):
        """Process PROIEL XML file into annotated text"""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            output_data = {
                'source': xml_file.name,
                'sentences': [],
                'tokens': [],
                'annotations': []
            }
            
            # Extract sentences and tokens
            for source in root.findall('.//source'):
                for div in source.findall('.//div'):
                    for sentence in div.findall('.//sentence'):
                        sent_data = {
                            'id': sentence.get('id'),
                            'tokens': []
                        }
                        
                        for token in sentence.findall('.//token'):
                            token_data = {
                                'id': token.get('id'),
                                'form': token.get('form'),
                                'lemma': token.get('lemma'),
                                'part_of_speech': token.get('part-of-speech'),
                                'morphology': token.get('morphology'),
                                'head_id': token.get('head-id'),
                                'relation': token.get('relation')
                            }
                            
                            # Extract valency information
                            if token.get('relation') in ['PRED', 'XOBJ', 'OBJ', 'OBL']:
                                token_data['valency_role'] = token.get('relation')
                                
                            sent_data['tokens'].append(token_data)
                            
                        output_data['sentences'].append(sent_data)
                        
            # Save as JSON
            output_file = self.output_path / f"{xml_file.stem}_PROIEL.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
                
            # Also create plain text version with annotations
            self.create_annotated_text(output_data, xml_file.stem)
            
            logging.info(f"✅ Processed PROIEL XML: {xml_file.name}")
            return True
            
        except Exception as e:
            logging.error(f"PROIEL processing error: {e}")
            return False
            
    def create_annotated_text(self, data, filename):
        """Create human-readable annotated text from PROIEL data"""
        output_lines = []
        
        for sentence in data['sentences']:
            # Original text
            text = ' '.join(t['form'] for t in sentence['tokens'] if t['form'])
            output_lines.append(f"\n[Sentence {sentence['id']}]")
            output_lines.append(text)
            
            # Grammatical annotation
            output_lines.append("\nAnnotations:")
            for token in sentence['tokens']:
                if token['form'] and token['lemma']:
                    annotation = f"  {token['form']} : {token['lemma']} ({token['part_of_speech']})"
                    if token.get('valency_role'):
                        annotation += f" [VALENCY: {token['valency_role']}]"
                    output_lines.append(annotation)
                    
        # Save annotated text
        output_file = self.output_path / f"{filename}_annotated.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
            
    def scan_for_xml_files(self):
        """Find and process all XML files"""
        xml_files = list(self.xml_path.glob('*.xml'))
        
        for xml_file in xml_files:
            if 'PROIEL' in xml_file.name or xml_file.suffix == '.xml':
                self.process_proiel_xml(xml_file)
                
        return len(xml_files)