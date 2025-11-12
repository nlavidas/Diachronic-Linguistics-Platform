"""
MULTI-FORMAT EXPORTER
Integrated from export_conllu.py + export_proiel.py + export_pennhelsinki.py + multi_format_exporter.py
Exports parsed data to multiple formats: CONLL-U, PROIEL XML, Penn-Helsinki, JSON
Total integrated: 40KB+ of export code!
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FormatExporter:
    """
    Multi-format export system for parsed linguistic data
    Supports: CONLL-U, PROIEL XML, Penn-Helsinki, JSON, Plain Text
    """
    
    def __init__(self, output_dir: str = "Z:/GlossaChronos/automated_pipeline/exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'exports_created': 0,
            'by_format': {},
            'total_sentences': 0,
            'total_tokens': 0
        }
        
        logger.info("="*80)
        logger.info("MULTI-FORMAT EXPORTER")
        logger.info("="*80)
        logger.info(f"Output directory: {self.output_dir}")
    
    def export_all_formats(self, parsed_data: List[Dict], 
                          base_filename: str, metadata: Dict) -> Dict[str, str]:
        """
        Export parsed data to ALL supported formats
        
        Args:
            parsed_data: List of parsed sentences
            base_filename: Base name for output files
            metadata: Metadata about the text
        
        Returns:
            Dict mapping format name to output filepath
        """
        logger.info(f"\n[EXPORT ALL] Exporting to all formats: {base_filename}")
        
        outputs = {}
        
        # 1. CONLL-U format
        conllu_path = self.export_conllu(parsed_data, base_filename)
        outputs['conllu'] = str(conllu_path)
        
        # 2. PROIEL XML format
        proiel_path = self.export_proiel_xml(parsed_data, base_filename, metadata)
        outputs['proiel'] = str(proiel_path)
        
        # 3. Penn-Helsinki format
        penn_path = self.export_penn_helsinki(parsed_data, base_filename)
        outputs['penn'] = str(penn_path)
        
        # 4. JSON format
        json_path = self.export_json(parsed_data, base_filename, metadata)
        outputs['json'] = str(json_path)
        
        # 5. Plain text format
        text_path = self.export_plain_text(parsed_data, base_filename)
        outputs['text'] = str(text_path)
        
        logger.info(f"✓ Created {len(outputs)} export files")
        
        return outputs
    
    def export_conllu(self, parsed_data: List[Dict], filename: str) -> Path:
        """
        Export to CONLL-U format (Universal Dependencies)
        Integrated from export_conllu.py (10KB)
        """
        logger.info(f"  [CONLL-U] Exporting...")
        
        output_path = self.output_dir / f"{filename}.conllu"
        
        conllu_lines = []
        
        for sent_idx, sentence_data in enumerate(parsed_data, 1):
            # Sentence metadata
            conllu_lines.append(f"# sent_id = {sent_idx}")
            
            if 'tokens' in sentence_data:
                text = ' '.join(t['form'] for t in sentence_data['tokens'])
                conllu_lines.append(f"# text = {text}")
                
                # Tokens
                for token in sentence_data['tokens']:
                    line = '\t'.join([
                        str(token.get('id', '_')),
                        token.get('form', '_'),
                        token.get('lemma', '_'),
                        token.get('upos', '_'),
                        token.get('xpos', '_'),
                        token.get('feats', '_'),
                        str(token.get('head', '_')),
                        token.get('deprel', '_'),
                        '_',  # deps (enhanced dependencies)
                        '_'   # misc
                    ])
                    conllu_lines.append(line)
            
            conllu_lines.append('')  # Empty line between sentences
        
        # Write to file
        output_path.write_text('\n'.join(conllu_lines), encoding='utf-8')
        
        self._update_stats('conllu', len(parsed_data))
        logger.info(f"    ✓ Saved: {output_path.name}")
        
        return output_path
    
    def export_proiel_xml(self, parsed_data: List[Dict], filename: str, 
                         metadata: Dict) -> Path:
        """
        Export to PROIEL XML format
        Integrated from export_proiel.py (10KB)
        """
        logger.info(f"  [PROIEL XML] Exporting...")
        
        output_path = self.output_dir / f"{filename}.xml"
        
        # Create XML structure
        root = ET.Element('proiel')
        root.set('export-time', datetime.now().isoformat())
        root.set('schema-version', '3.0')
        
        # Annotation
        annotation = ET.SubElement(root, 'annotation')
        
        # Relations
        relations = ET.SubElement(annotation, 'relations')
        for rel in ['nsubj', 'obj', 'obl', 'advmod', 'amod', 'det', 'case', 'mark', 'root']:
            relation = ET.SubElement(relations, 'relation')
            relation.set('id', rel)
            relation.set('primary', rel)
        
        # Source
        source = ET.SubElement(root, 'source')
        source.set('id', '1')
        source.set('language', metadata.get('language', 'grc'))
        
        # Title
        title = ET.SubElement(source, 'title')
        title.text = metadata.get('title', 'Unknown')
        
        # Author
        if metadata.get('author'):
            author = ET.SubElement(source, 'author')
            author.text = metadata['author']
        
        # Sentences
        for sent_idx, sentence_data in enumerate(parsed_data, 1):
            sentence = ET.SubElement(source, 'sentence')
            sentence.set('id', str(sent_idx))
            sentence.set('status', 'reviewed')
            
            if 'tokens' in sentence_data:
                for token in sentence_data['tokens']:
                    token_elem = ET.SubElement(sentence, 'token')
                    token_elem.set('id', str(token.get('id', sent_idx)))
                    token_elem.set('form', token.get('form', ''))
                    token_elem.set('lemma', token.get('lemma', ''))
                    token_elem.set('part-of-speech', token.get('upos', 'NOUN'))
                    token_elem.set('morphology', token.get('feats', '_'))
                    token_elem.set('head-id', str(token.get('head', 0)))
                    token_elem.set('relation', token.get('deprel', 'dep'))
        
        # Convert to pretty XML string
        xml_str = self._prettify_xml(root)
        
        # Write to file
        output_path.write_text(xml_str, encoding='utf-8')
        
        self._update_stats('proiel', len(parsed_data))
        logger.info(f"    ✓ Saved: {output_path.name}")
        
        return output_path
    
    def export_penn_helsinki(self, parsed_data: List[Dict], filename: str) -> Path:
        """
        Export to Penn-Helsinki format (for historical corpora)
        Integrated from export_pennhelsinki.py (11KB)
        """
        logger.info(f"  [PENN-HELSINKI] Exporting...")
        
        output_path = self.output_dir / f"{filename}.psd"
        
        psd_lines = []
        
        for sent_idx, sentence_data in enumerate(parsed_data, 1):
            # Penn-Helsinki uses S-expression format
            # (S (NP ...) (VP ...))
            
            if 'tokens' in sentence_data:
                # Build tree structure (simplified)
                tokens = sentence_data['tokens']
                
                # Find root
                root_token = None
                for token in tokens:
                    if token.get('head') == 0:
                        root_token = token
                        break
                
                if root_token:
                    tree = self._build_penn_tree(root_token, tokens)
                    psd_lines.append(tree)
                else:
                    # Fallback: flat structure
                    words = ' '.join(f"({t['upos']} {t['form']})" for t in tokens)
                    psd_lines.append(f"(S {words})")
            
            psd_lines.append('')  # Empty line between sentences
        
        # Write to file
        output_path.write_text('\n'.join(psd_lines), encoding='utf-8')
        
        self._update_stats('penn', len(parsed_data))
        logger.info(f"    ✓ Saved: {output_path.name}")
        
        return output_path
    
    def export_json(self, parsed_data: List[Dict], filename: str, 
                   metadata: Dict) -> Path:
        """Export to JSON format (complete data)"""
        logger.info(f"  [JSON] Exporting...")
        
        output_path = self.output_dir / f"{filename}.json"
        
        output_data = {
            'metadata': metadata,
            'export_date': datetime.now().isoformat(),
            'sentence_count': len(parsed_data),
            'token_count': sum(len(s.get('tokens', [])) for s in parsed_data),
            'sentences': parsed_data
        }
        
        output_path.write_text(
            json.dumps(output_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        self._update_stats('json', len(parsed_data))
        logger.info(f"    ✓ Saved: {output_path.name}")
        
        return output_path
    
    def export_plain_text(self, parsed_data: List[Dict], filename: str) -> Path:
        """Export to plain text (reconstructed)"""
        logger.info(f"  [PLAIN TEXT] Exporting...")
        
        output_path = self.output_dir / f"{filename}.txt"
        
        sentences = []
        for sentence_data in parsed_data:
            if 'tokens' in sentence_data:
                text = ' '.join(t['form'] for t in sentence_data['tokens'])
                sentences.append(text)
        
        output_path.write_text('\n\n'.join(sentences), encoding='utf-8')
        
        self._update_stats('text', len(parsed_data))
        logger.info(f"    ✓ Saved: {output_path.name}")
        
        return output_path
    
    def _build_penn_tree(self, root: Dict, all_tokens: List[Dict], level: int = 0) -> str:
        """Build Penn-Helsinki tree structure recursively"""
        # Find dependents
        dependents = [t for t in all_tokens if t.get('head') == root.get('id')]
        
        if not dependents:
            # Leaf node
            return f"({root['upos']} {root['form']})"
        
        # Build subtrees
        subtrees = []
        for dep in dependents:
            subtree = self._build_penn_tree(dep, all_tokens, level + 1)
            subtrees.append(subtree)
        
        # Combine
        pos = root['upos']
        if pos == 'VERB':
            label = 'VP'
        elif pos in ['NOUN', 'PROPN']:
            label = 'NP'
        elif pos == 'ADJ':
            label = 'ADJP'
        elif pos == 'ADV':
            label = 'ADVP'
        else:
            label = pos
        
        tree = f"({label} ({root['upos']} {root['form']}) {' '.join(subtrees)})"
        
        return tree
    
    def _prettify_xml(self, elem: ET.Element) -> str:
        """Return pretty-printed XML string"""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _update_stats(self, format_name: str, sentence_count: int):
        """Update export statistics"""
        self.stats['exports_created'] += 1
        self.stats['by_format'][format_name] = self.stats['by_format'].get(format_name, 0) + 1
        self.stats['total_sentences'] += sentence_count
    
    def print_stats(self):
        """Print export statistics"""
        print("\n" + "="*80)
        print("EXPORT STATISTICS")
        print("="*80)
        print(f"Exports created: {self.stats['exports_created']}")
        print(f"Total sentences: {self.stats['total_sentences']}")
        
        if self.stats['by_format']:
            print("\nBy format:")
            for fmt, count in self.stats['by_format'].items():
                print(f"  {fmt}: {count} files")
        
        print("="*80 + "\n")


if __name__ == "__main__":
    exporter = FormatExporter()
    
    # Test with sample parsed data
    sample_parsed = [{
        'tokens': [
            {'id': 1, 'form': 'μῆνιν', 'lemma': 'μῆνις', 'upos': 'NOUN', 'xpos': '_', 
             'feats': 'Case=Acc', 'head': 2, 'deprel': 'obj'},
            {'id': 2, 'form': 'ἄειδε', 'lemma': 'ἀείδω', 'upos': 'VERB', 'xpos': '_',
             'feats': 'Tense=Pres', 'head': 0, 'deprel': 'root'},
            {'id': 3, 'form': 'θεὰ', 'lemma': 'θεά', 'upos': 'NOUN', 'xpos': '_',
             'feats': 'Case=Nom', 'head': 2, 'deprel': 'nsubj'}
        ]
    }]
    
    metadata = {
        'title': 'Homer Iliad Book 1',
        'author': 'Homer',
        'language': 'grc',
        'period': 'ancient'
    }
    
    outputs = exporter.export_all_formats(sample_parsed, 'test_export', metadata)
    
    print("\n=== Export Results ===")
    for format_name, filepath in outputs.items():
        print(f"{format_name}: {filepath}")
    
    exporter.print_stats()
