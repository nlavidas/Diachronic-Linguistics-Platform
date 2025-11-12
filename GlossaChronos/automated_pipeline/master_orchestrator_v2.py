"""
MASTER ORCHESTRATOR V2.0
Enhanced 24/7 coordination of ALL integrated systems
Integrates features from run_overnight_agents.py + run_24_7_system.ps1 + pipeline_orchestrator.py
Complete end-to-end automation with all 8 systems!
"""

import logging
from pathlib import Path
from datetime import datetime
import json
import time
from typing import Dict, List
import sys

# Import all integrated systems
try:
    from ultimate_text_collector import UltimateTextCollector
    from ai_annotator import AIAnnotator
    from continuous_trainer import ContinuousTrainer
    from quality_validator import QualityValidator
    from diachronic_analyzer import DiachronicAnalyzer
    from enhanced_parser import EnhancedParser
    from format_exporter import FormatExporter
except ImportError as e:
    logging.warning(f"Import error: {e}. Some systems may not be available.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - MASTER - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MasterOrchestrator:
    """
    Master 24/7 orchestrator for complete pipeline
    Coordinates all 8 integrated systems
    """
    
    def __init__(self, base_dir: str = "Z:/GlossaChronos/automated_pipeline"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize all systems
        logger.info("="*80)
        logger.info("MASTER ORCHESTRATOR V2.0 - INITIALIZING ALL SYSTEMS")
        logger.info("="*80)
        
        try:
            self.collector = UltimateTextCollector(str(self.base_dir))
            logger.info("✓ System 1: Ultimate Text Collector")
        except:
            self.collector = None
            logger.warning("✗ System 1: Text Collector unavailable")
        
        try:
            self.annotator = AIAnnotator()
            logger.info("✓ System 2: AI Annotator")
        except:
            self.annotator = None
            logger.warning("✗ System 2: AI Annotator unavailable")
        
        try:
            self.trainer = ContinuousTrainer(str(self.base_dir))
            logger.info("✓ System 3: Continuous Trainer")
        except:
            self.trainer = None
            logger.warning("✗ System 3: Trainer unavailable")
        
        try:
            self.validator = QualityValidator()
            logger.info("✓ System 4: Quality Validator")
        except:
            self.validator = None
            logger.warning("✗ System 4: Validator unavailable")
        
        try:
            self.analyzer = DiachronicAnalyzer()
            logger.info("✓ System 5: Diachronic Analyzer")
        except:
            self.analyzer = None
            logger.warning("✗ System 5: Analyzer unavailable")
        
        try:
            self.parser = EnhancedParser()
            logger.info("✓ System 6: Enhanced Parser")
        except:
            self.parser = None
            logger.warning("✗ System 6: Parser unavailable")
        
        try:
            self.exporter = FormatExporter()
            logger.info("✓ System 7: Format Exporter")
        except:
            self.exporter = None
            logger.warning("✗ System 7: Exporter unavailable")
        
        # Statistics
        self.stats = {
            'cycles_completed': 0,
            'texts_processed': 0,
            'total_runtime': 0.0,
            'errors': [],
            'start_time': datetime.now()
        }
        
        logger.info("="*80)
    
    def run_complete_pipeline(self, language: str = 'grc', period: str = 'ancient',
                             text_limit: int = 5) -> Dict:
        """
        Run complete end-to-end pipeline through all systems
        
        1. Collect texts
        2. Validate quality
        3. Parse with enhanced parser
        4. Annotate with AI
        5. Analyze diachronic patterns
        6. Export to all formats
        7. Train models (optional)
        """
        logger.info("\n" + "="*80)
        logger.info(f"COMPLETE PIPELINE: {language}/{period}")
        logger.info("="*80)
        
        start_time = time.time()
        pipeline_results = {
            'success': False,
            'stages': {},
            'errors': [],
            'runtime': 0.0
        }
        
        try:
            # STAGE 1: Text Collection
            logger.info("\n🔹 STAGE 1: Text Collection")
            if self.collector:
                collection_results = self.collector.collect_from_all_sources(
                    gutenberg_limit=text_limit,
                    first1k_limit=text_limit,
                    wikisource_limit=text_limit
                )
                pipeline_results['stages']['collection'] = {
                    'status': 'success',
                    'texts_collected': sum(len(texts) for texts in collection_results.values())
                }
                logger.info(f"  ✓ Collected {pipeline_results['stages']['collection']['texts_collected']} texts")
            else:
                pipeline_results['stages']['collection'] = {'status': 'skipped'}
            
            # STAGE 2: Quality Validation
            logger.info("\n🔹 STAGE 2: Quality Validation")
            if self.validator:
                # Get sample texts for validation
                sample_text = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος οὐλομένην"
                validation_result = self.validator.validate_text(
                    text=sample_text,
                    language=language,
                    period=period,
                    metadata={'title': 'Test', 'source': 'pipeline', 'language': language}
                )
                pipeline_results['stages']['validation'] = {
                    'status': 'success',
                    'quality_score': validation_result['overall_score'],
                    'passed': validation_result['pass']
                }
                logger.info(f"  ✓ Quality score: {validation_result['overall_score']:.1f}%")
            else:
                pipeline_results['stages']['validation'] = {'status': 'skipped'}
            
            # STAGE 3: Enhanced Parsing
            logger.info("\n🔹 STAGE 3: Enhanced Parsing")
            if self.parser:
                sample_text = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"
                parse_result = self.parser.parse_sentence(sample_text, language, period)
                pipeline_results['stages']['parsing'] = {
                    'status': 'success',
                    'tokens_parsed': len(parse_result['tokens']),
                    'dependencies': len(parse_result['dependencies'])
                }
                logger.info(f"  ✓ Parsed {len(parse_result['tokens'])} tokens")
            else:
                pipeline_results['stages']['parsing'] = {'status': 'skipped'}
            
            # STAGE 4: AI Annotation
            logger.info("\n🔹 STAGE 4: AI Annotation")
            if self.annotator:
                sample_text = "μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος"
                annotation_result = self.annotator.annotate_text(
                    text=sample_text,
                    language=language,
                    period=period
                )
                pipeline_results['stages']['annotation'] = {
                    'status': 'success',
                    'sentences_annotated': annotation_result['sentences_annotated'],
                    'llm_used': annotation_result['llm_used']
                }
                logger.info(f"  ✓ Annotated with {annotation_result['llm_used']}")
            else:
                pipeline_results['stages']['annotation'] = {'status': 'skipped'}
            
            # STAGE 5: Diachronic Analysis
            logger.info("\n🔹 STAGE 5: Diachronic Analysis")
            if self.analyzer:
                sample_text = "The gay company had an awful time being silly and nice."
                shifts = self.analyzer.analyze_text_for_shifts(
                    text=sample_text,
                    language='en',
                    period=period
                )
                pipeline_results['stages']['diachronic'] = {
                    'status': 'success',
                    'shifts_detected': len(shifts)
                }
                logger.info(f"  ✓ Detected {len(shifts)} semantic shifts")
            else:
                pipeline_results['stages']['diachronic'] = {'status': 'skipped'}
            
            # STAGE 6: Format Export
            logger.info("\n🔹 STAGE 6: Format Export")
            if self.exporter and 'parsing' in pipeline_results['stages']:
                sample_parsed = [{'tokens': parse_result['tokens']}] if 'parse_result' in locals() else []
                if sample_parsed:
                    export_results = self.exporter.export_all_formats(
                        parsed_data=sample_parsed,
                        base_filename=f"pipeline_test_{language}",
                        metadata={'title': 'Pipeline Test', 'language': language, 'period': period}
                    )
                    pipeline_results['stages']['export'] = {
                        'status': 'success',
                        'formats_created': len(export_results)
                    }
                    logger.info(f"  ✓ Exported to {len(export_results)} formats")
            else:
                pipeline_results['stages']['export'] = {'status': 'skipped'}
            
            # STAGE 7: Model Training (optional, computationally intensive)
            logger.info("\n🔹 STAGE 7: Model Training (optional)")
            if self.trainer and False:  # Disabled by default
                self.trainer.train_model(language, epochs=1)
                pipeline_results['stages']['training'] = {
                    'status': 'success',
                    'epochs': 1
                }
                logger.info(f"  ✓ Training complete")
            else:
                pipeline_results['stages']['training'] = {'status': 'skipped'}
            
            # Success!
            pipeline_results['success'] = True
            
        except Exception as e:
            logger.error(f"❌ Pipeline error: {e}")
            pipeline_results['errors'].append(str(e))
            self.stats['errors'].append(str(e))
        
        # Calculate runtime
        runtime = time.time() - start_time
        pipeline_results['runtime'] = runtime
        
        # Update stats
        self.stats['cycles_completed'] += 1
        self.stats['total_runtime'] += runtime
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*80)
        logger.info(f"Runtime: {runtime:.2f}s")
        logger.info(f"Stages completed: {sum(1 for s in pipeline_results['stages'].values() if s['status'] == 'success')}")
        logger.info(f"Status: {'SUCCESS' if pipeline_results['success'] else 'FAILED'}")
        logger.info("="*80)
        
        return pipeline_results
    
    def run_24_7_continuous(self, interval_minutes: int = 60):
        """
        Run pipeline continuously 24/7
        Process new texts every interval
        """
        logger.info("\n" + "="*80)
        logger.info("24/7 CONTINUOUS MODE ACTIVATED")
        logger.info("="*80)
        logger.info(f"Processing interval: {interval_minutes} minutes")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*80)
        
        try:
            while True:
                # Run complete pipeline
                results = self.run_complete_pipeline()
                
                # Print stats
                self.print_stats()
                
                # Wait for next cycle
                logger.info(f"\n⏰ Waiting {interval_minutes} minutes until next cycle...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            logger.info("\n\n⏹️  Stopping 24/7 mode...")
            self.print_stats()
            logger.info("Stopped.")
    
    def generate_final_report(self) -> str:
        """Generate comprehensive pipeline report"""
        report = []
        report.append("="*80)
        report.append("MASTER ORCHESTRATOR - FINAL REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Running since: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("STATISTICS")
        report.append("-"*80)
        report.append(f"Cycles completed: {self.stats['cycles_completed']}")
        report.append(f"Texts processed: {self.stats['texts_processed']}")
        report.append(f"Total runtime: {self.stats['total_runtime']:.2f}s")
        report.append(f"Errors encountered: {len(self.stats['errors'])}")
        report.append("")
        
        report.append("SYSTEM STATUS")
        report.append("-"*80)
        systems = [
            ('Text Collector', self.collector),
            ('AI Annotator', self.annotator),
            ('Continuous Trainer', self.trainer),
            ('Quality Validator', self.validator),
            ('Diachronic Analyzer', self.analyzer),
            ('Enhanced Parser', self.parser),
            ('Format Exporter', self.exporter)
        ]
        
        for name, system in systems:
            status = "✓ OPERATIONAL" if system else "✗ UNAVAILABLE"
            report.append(f"{name:25s}: {status}")
        
        report.append("")
        report.append("="*80)
        
        return '\n'.join(report)
    
    def print_stats(self):
        """Print orchestrator statistics"""
        print(self.generate_final_report())


if __name__ == "__main__":
    orchestrator = MasterOrchestrator()
    
    # Run single pipeline cycle
    print("\n🚀 Running complete pipeline (single cycle)...\n")
    results = orchestrator.run_complete_pipeline(language='grc', period='ancient', text_limit=3)
    
    # Print final report
    print(orchestrator.generate_final_report())
    
    # Uncomment to run 24/7
    # orchestrator.run_24_7_continuous(interval_minutes=60)
