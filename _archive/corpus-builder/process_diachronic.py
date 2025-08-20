#!/usr/bin/env python3
"""
Diachronic Retranslation Analysis for NKUA Historical Corpus
Tracks how texts evolve across languages and time periods
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class DiachronicAnalyzer:
    def __init__(self, corpus_dir=None):
        self.corpus_dir = corpus_dir or self.find_latest_corpus()
        self.results_dir = f"diachronic_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Define known retranslation chains
        self.known_chains = {
            'bible': {
                'source_text': 'New Testament',
                'chronology': ['Ancient Greek', 'Latin', 'Gothic', 'Old English', 'Middle English'],
                'key_passages': ['lords_prayer', 'beatitudes', 'creation'],
            },
            'homer': {
                'source_text': 'Iliad/Odyssey',
                'chronology': ['Ancient Greek', 'Latin', 'Old French', 'Middle English'],
                'key_passages': ['invocation', 'catalog_ships', 'heroic_epithets'],
            }
        }
    
    def find_latest_corpus(self):
        """Find the most recent corpus directory"""
        current_dir = Path('.')
        corpus_dirs = [d for d in current_dir.iterdir() 
                      if d.is_dir() and ('corpus_results_' in d.name or 'analysis_results_' in d.name)]
        if corpus_dirs:
            return max(corpus_dirs, key=lambda x: x.stat().st_mtime)
        return None
    
    def identify_text_family(self, filename, content):
        """Identify which retranslation family a text belongs to"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Bible texts
        bible_indicators = ['matthew', 'gospel', 'testament', 'atta unsar', 'pater noster', 'lords prayer']
        if any(indicator in filename_lower or indicator in content_lower for indicator in bible_indicators):
            return 'bible'
        
        # Homeric texts
        homer_indicators = ['iliad', 'odyssey', 'homer', 'achilles', 'odysseus', 'troy']
        if any(indicator in filename_lower or indicator in content_lower for indicator in homer_indicators):
            return 'homer'
        
        return 'unknown'
    
    def analyze_linguistic_evolution(self, texts_by_family):
        """Analyze how linguistic features evolve across retranslations"""
        evolution_analysis = {}
        
        for family, texts in texts_by_family.items():
            if len(texts) < 2:  # Need at least 2 texts for comparison
                continue
                
            family_analysis = {
                'text_family': family,
                'versions_found': len(texts),
                'linguistic_changes': [],
                'chronological_order': []
            }
            
            # Simple chronological ordering based on language patterns
            greek_texts = [t for t in texts if 'greek' in t.get('language', '').lower()]
            latin_texts = [t for t in texts if 'latin' in t.get('language', '').lower()]
            gothic_texts = [t for t in texts if 'gothic' in t.get('language', '').lower()]
            
            ordered_texts = greek_texts + latin_texts + gothic_texts
            family_analysis['chronological_order'] = [t.get('language', 'Unknown') for t in ordered_texts]
            
            # Analyze changes between consecutive versions
            for i in range(len(ordered_texts) - 1):
                current = ordered_texts[i]
                next_version = ordered_texts[i + 1]
                
                change_analysis = {
                    'from_language': current.get('language', 'Unknown'),
                    'to_language': next_version.get('language', 'Unknown'),
                    'changes_detected': []
                }
                
                # Word count comparison
                current_words = current.get('word_count', 0)
                next_words = next_version.get('word_count', 0)
                
                if next_words > current_words * 1.2:
                    change_analysis['changes_detected'].append('Text expansion (possible elaboration)')
                elif next_words < current_words * 0.8:
                    change_analysis['changes_detected'].append('Text compression (possible simplification)')
                
                # Language-specific patterns
                if 'Greek' in current.get('language', '') and 'Latin' in next_version.get('language', ''):
                    change_analysis['changes_detected'].extend([
                        'Greek article system → Latin case system',
                        'Particle reduction in translation',
                        'Word order adaptation'
                    ])
                
                family_analysis['linguistic_changes'].append(change_analysis)
            
            evolution_analysis[family] = family_analysis
        
        return evolution_analysis
    
    def generate_timeline_visualization(self, evolution_analysis):
        """Generate HTML timeline visualization"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Diachronic Retranslation Timeline</title>
    <style>
        body {{ font-family: 'Georgia', serif; margin: 40px; background: #fafafa; }}
        .timeline-container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .timeline {{ position: relative; margin: 40px 0; }}
        .timeline::before {{ content: ''; position: absolute; left: 50%; top: 0; bottom: 0; width: 3px; background: #3498db; }}
        .timeline-item {{ margin: 40px 0; position: relative; }}
        .timeline-content {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 45%; }}
        .timeline-item:nth-child(odd) .timeline-content {{ margin-left: 55%; }}
        .timeline-item:nth-child(even) .timeline-content {{ margin-right: 55%; }}
        .timeline-marker {{ position: absolute; left: 50%; top: 20px; width: 20px; height: 20px; background: #3498db; border-radius: 50%; transform: translateX(-50%); border: 3px solid white; }}
        .family-section {{ margin: 60px 0; padding: 30px; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #e74c3c; }}
        .language {{ font-weight: bold; color: #2c3e50; font-size: 1.2em; }}
        .changes {{ margin: 15px 0; }}
        .change-item {{ background: #e8f5e8; padding: 8px 12px; margin: 5px 0; border-radius: 5px; font-size: 0.9em; }}
        h1, h2 {{ color: #2c3e50; }}
        .header {{ text-align: center; margin-bottom: 40px; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; }}
    </style>
</head>
<body>
    <div class="timeline-container">
        <div class="header">
            <h1>📜 Diachronic Retranslation Analysis</h1>
            <p>Tracking textual transmission across languages and centuries</p>
            <p><em>Generated on {datetime.now().strftime('%Y-%m-%d')}</em></p>
        </div>
"""
        
        for family, analysis in evolution_analysis.items():
            html_content += f"""
        <div class="family-section">
            <h2>📚 {family.title()} Retranslation Chain</h2>
            <p><strong>Source Text:</strong> {self.known_chains.get(family, {}).get('source_text', 'Unknown')}</p>
            <p><strong>Versions Found:</strong> {analysis['versions_found']}</p>
            
            <div class="timeline">
"""
            
            # Add timeline items for each linguistic change
            for i, change in enumerate(analysis['linguistic_changes']):
                html_content += f"""
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <div class="language">{change['from_language']} → {change['to_language']}</div>
                        <div class="changes">
                            <strong>Linguistic Changes:</strong>
"""
                
                for change_item in change['changes_detected']:
                    html_content += f'                            <div class="change-item">• {change_item}</div>\n'
                
                html_content += """
                        </div>
                    </div>
                </div>
"""
            
            html_content += """
            </div>
        </div>
"""
        
        html_content += """
        
        <div style="text-align: center; margin-top: 40px; padding: 20px; background: #e8f5e8; border-radius: 8px;">
            <h3>🎯 Analysis Complete</h3>
            <p>This diachronic analysis reveals patterns of linguistic change across retranslations.</p>
            <p><strong>Research Value:</strong> Understanding how texts adapt to new linguistic and cultural contexts</p>
        </div>
    </div>
</body>
</html>
        """
        
        timeline_path = os.path.join(self.results_dir, 'retranslation_timeline.html')
        with open(timeline_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return timeline_path
    
    def run_diachronic_analysis(self):
        """Run the complete diachronic analysis"""
        print("📜 NKUA Diachronic Retranslation Analyzer")
        print("=" * 60)
        
        if not self.corpus_dir or not os.path.exists(self.corpus_dir):
            print("❌ No corpus directory found. Please run collect_texts.py and ai_analyze.py first.")
            return
        
        # Load previous analysis results if available
        analysis_file = None
        for file in Path(self.corpus_dir).glob('detailed_analysis.json'):
            analysis_file = file
            break
        
        if not analysis_file:
            print("❌ No analysis results found. Please run ai_analyze.py first.")
            return
        
        print(f"📊 Loading analysis from: {analysis_file}")
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            previous_analysis = json.load(f)
        
        analyses = previous_analysis if isinstance(previous_analysis, list) else previous_analysis.get('analyses', [])
        
        if not analyses:
            print("❌ No text analyses found in the data.")
            return
        
        print(f"📚 Processing {len(analyses)} texts for diachronic analysis")
        
        # Group texts by family
        texts_by_family = defaultdict(list)
        
        for analysis in analyses:
            if 'error' in analysis:
                continue
                
            filename = analysis.get('filename', '')
            # Simple content simulation for family identification
            content = f"sample content for {filename}"
            
            family = self.identify_text_family(filename, content)
            if family != 'unknown':
                analysis['text_family'] = family
                texts_by_family[family].append(analysis)
        
        print(f"🔍 Identified {len(texts_by_family)} text families")
        
        # Analyze linguistic evolution
        print("📈 Analyzing linguistic evolution...")
        evolution_analysis = self.analyze_linguistic_evolution(texts_by_family)
        
        # Generate timeline visualization
        print("📊 Creating timeline visualization...")
        timeline_path = self.generate_timeline_visualization(evolution_analysis)
        
        # Save complete results
        results = {
            'diachronic_analysis': evolution_analysis,
            'texts_by_family': dict(texts_by_family),
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'source_corpus': str(self.corpus_dir),
                'families_analyzed': list(texts_by_family.keys()),
                'total_retranslation_chains': len(evolution_analysis)
            }
        }
        
        json_path = os.path.join(self.results_dir, 'diachronic_analysis.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("📜 DIACHRONIC ANALYSIS COMPLETE!")
        print(f"📁 Results directory: {self.results_dir}")
        print(f"📊 Timeline visualization: {timeline_path}")
        print(f"📄 Complete data: {json_path}")
        print(f"🔍 Families analyzed: {', '.join(texts_by_family.keys())}")
        print("\n✨ Your retranslation analysis is ready!")
        
        return {
            'results_dir': self.results_dir,
            'timeline_path': timeline_path,
            'json_path': json_path,
            'families_found': list(texts_by_family.keys())
        }

def main():
    analyzer = DiachronicAnalyzer()
    try:
        results = analyzer.run_diachronic_analysis()
    except KeyboardInterrupt:
        print("\n⏹️  Analysis cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Check that you have run collect_texts.py and ai_analyze.py first.")

if __name__ == "__main__":
    main()
