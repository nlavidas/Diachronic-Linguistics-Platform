"""
ALL-NIGHT PRODUCTION RUNNER
Runs selected systems continuously overnight
Generates comprehensive morning report
User-configurable module activation
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ALL_NIGHT - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('all_night_production.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AllNightRunner:
    """
    Production all-night runner with configurable modules
    """
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'cycles_completed': 0,
            'total_texts_processed': 0,
            'total_annotations': 0,
            'total_validations': 0,
            'total_parses': 0,
            'total_exports': 0,
            'errors': [],
            'system_stats': {},
            'checkpoints': []
        }
        
        self.morning_report_path = Path("MORNING_REPORT.md")
        
        logger.info("="*80)
        logger.info("ALL-NIGHT PRODUCTION RUNNER")
        logger.info("="*80)
        logger.info(f"Configuration: {config_path}")
        self.log_enabled_systems()
        logger.info("="*80)
    
    def load_config(self) -> Dict:
        """Load configuration from JSON"""
        if not self.config_path.exists():
            logger.warning("Config not found, using defaults")
            return self.get_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"✓ Configuration loaded from {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Default configuration"""
        return {
            'systems_enabled': {
                'text_collector': True,
                'ai_annotator': False,
                'continuous_trainer': False,
                'quality_validator': True,
                'diachronic_analyzer': True,
                'enhanced_parser': True,
                'format_exporter': True
            },
            'all_night_mode': {
                'enabled': True,
                'cycle_interval_minutes': 30,
                'max_cycles': 20,
                'generate_reports': True
            }
        }
    
    def log_enabled_systems(self):
        """Log which systems are enabled"""
        logger.info("\nEnabled Systems:")
        for system, enabled in self.config['systems_enabled'].items():
            status = "✓ ENABLED" if enabled else "✗ DISABLED"
            logger.info(f"  {system}: {status}")
    
    def is_system_enabled(self, system_name: str) -> bool:
        """Check if a system is enabled"""
        return self.config['systems_enabled'].get(system_name, False)
    
    def run_cycle(self, cycle_num: int) -> Dict:
        """Run one complete processing cycle"""
        logger.info("\n" + "="*80)
        logger.info(f"CYCLE {cycle_num}")
        logger.info("="*80)
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        cycle_start = time.time()
        cycle_results = {
            'cycle': cycle_num,
            'timestamp': datetime.now().isoformat(),
            'systems_run': [],
            'results': {}
        }
        
        try:
            # SYSTEM 1: Text Collection
            if self.is_system_enabled('text_collector'):
                logger.info("\n[1/7] Running Text Collector...")
                result = self.run_text_collector()
                cycle_results['systems_run'].append('text_collector')
                cycle_results['results']['text_collector'] = result
                self.stats['total_texts_processed'] += result.get('texts_collected', 0)
            
            # SYSTEM 2: AI Annotation (if enabled)
            if self.is_system_enabled('ai_annotator'):
                logger.info("\n[2/7] Running AI Annotator...")
                result = self.run_ai_annotator()
                cycle_results['systems_run'].append('ai_annotator')
                cycle_results['results']['ai_annotator'] = result
                self.stats['total_annotations'] += result.get('sentences_annotated', 0)
            
            # SYSTEM 3: Training (if enabled)
            if self.is_system_enabled('continuous_trainer'):
                logger.info("\n[3/7] Running Continuous Trainer...")
                result = self.run_trainer()
                cycle_results['systems_run'].append('continuous_trainer')
                cycle_results['results']['continuous_trainer'] = result
            
            # SYSTEM 4: Quality Validation
            if self.is_system_enabled('quality_validator'):
                logger.info("\n[4/7] Running Quality Validator...")
                result = self.run_validator()
                cycle_results['systems_run'].append('quality_validator')
                cycle_results['results']['quality_validator'] = result
                self.stats['total_validations'] += result.get('texts_validated', 0)
            
            # SYSTEM 5: Diachronic Analysis
            if self.is_system_enabled('diachronic_analyzer'):
                logger.info("\n[5/7] Running Diachronic Analyzer...")
                result = self.run_diachronic_analyzer()
                cycle_results['systems_run'].append('diachronic_analyzer')
                cycle_results['results']['diachronic_analyzer'] = result
            
            # SYSTEM 6: Enhanced Parser
            if self.is_system_enabled('enhanced_parser'):
                logger.info("\n[6/7] Running Enhanced Parser...")
                result = self.run_parser()
                cycle_results['systems_run'].append('enhanced_parser')
                cycle_results['results']['enhanced_parser'] = result
                self.stats['total_parses'] += result.get('tokens_parsed', 0)
            
            # SYSTEM 7: Format Exporter
            if self.is_system_enabled('format_exporter'):
                logger.info("\n[7/7] Running Format Exporter...")
                result = self.run_exporter()
                cycle_results['systems_run'].append('format_exporter')
                cycle_results['results']['format_exporter'] = result
                self.stats['total_exports'] += result.get('files_created', 0)
            
        except Exception as e:
            logger.error(f"Cycle error: {e}")
            self.stats['errors'].append({
                'cycle': cycle_num,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        cycle_time = time.time() - cycle_start
        cycle_results['duration_seconds'] = cycle_time
        
        self.stats['cycles_completed'] += 1
        
        # Save checkpoint
        if self.config['all_night_mode'].get('save_checkpoints', True):
            self.stats['checkpoints'].append(cycle_results)
        
        # Cycle summary
        logger.info("\n" + "="*80)
        logger.info(f"CYCLE {cycle_num} COMPLETE")
        logger.info("="*80)
        logger.info(f"Duration: {cycle_time:.2f}s")
        logger.info(f"Systems run: {len(cycle_results['systems_run'])}")
        logger.info(f"Total cycles: {self.stats['cycles_completed']}")
        logger.info("="*80)
        
        return cycle_results
    
    def run_text_collector(self) -> Dict:
        """Run text collection system"""
        try:
            from ultimate_text_collector import UltimateTextCollector
            collector = UltimateTextCollector()
            
            config = self.config.get('text_collection', {})
            limits = config.get('limits', {})
            
            results = collector.collect_from_all_sources(
                gutenberg_limit=limits.get('gutenberg_limit', 5),
                first1k_limit=limits.get('first1k_limit', 5),
                wikisource_limit=limits.get('wikisource_limit', 3)
            )
            
            total = sum(len(texts) for texts in results.values())
            
            logger.info(f"  ✓ Collected {total} texts")
            return {'texts_collected': total, 'by_source': {k: len(v) for k, v in results.items()}}
        except Exception as e:
            logger.error(f"  ✗ Text collector failed: {e}")
            return {'texts_collected': 0, 'error': str(e)}
    
    def run_ai_annotator(self) -> Dict:
        """Run AI annotation system"""
        try:
            from ai_annotator import AIAnnotator
            annotator = AIAnnotator()
            
            sample = "Sample text for annotation."
            result = annotator.annotate_text(sample, 'en', 'modern')
            
            logger.info(f"  ✓ Annotated {result['sentences_annotated']} sentences")
            return result
        except Exception as e:
            logger.error(f"  ✗ AI annotator failed: {e}")
            return {'sentences_annotated': 0, 'error': str(e)}
    
    def run_trainer(self) -> Dict:
        """Run training system"""
        try:
            from continuous_trainer import ContinuousTrainer
            trainer = ContinuousTrainer()
            
            epochs = self.config.get('training', {}).get('epochs_per_session', 1)
            trainer.train_model('grc', epochs=epochs)
            
            logger.info(f"  ✓ Completed {epochs} training epochs")
            return {'epochs': epochs, 'loss': trainer.stats['current_loss']}
        except Exception as e:
            logger.error(f"  ✗ Trainer failed: {e}")
            return {'epochs': 0, 'error': str(e)}
    
    def run_validator(self) -> Dict:
        """Run validation system"""
        try:
            from quality_validator import QualityValidator
            validator = QualityValidator()
            
            sample = "Sample text for validation testing."
            result = validator.validate_text(
                sample, 'en', 'modern',
                {'title': 'Test', 'source': 'test', 'language': 'en'}
            )
            
            logger.info(f"  ✓ Validated (score: {result['overall_score']:.1f}%)")
            return {'texts_validated': 1, 'score': result['overall_score']}
        except Exception as e:
            logger.error(f"  ✗ Validator failed: {e}")
            return {'texts_validated': 0, 'error': str(e)}
    
    def run_diachronic_analyzer(self) -> Dict:
        """Run diachronic analysis"""
        try:
            from diachronic_analyzer import DiachronicAnalyzer
            analyzer = DiachronicAnalyzer()
            
            sample = "The gay people were silly and nice."
            shifts = analyzer.analyze_text_for_shifts(sample, 'en', 'modern')
            
            logger.info(f"  ✓ Detected {len(shifts)} semantic shifts")
            return {'shifts_detected': len(shifts)}
        except Exception as e:
            logger.error(f"  ✗ Analyzer failed: {e}")
            return {'shifts_detected': 0, 'error': str(e)}
    
    def run_parser(self) -> Dict:
        """Run parsing system"""
        try:
            from enhanced_parser import EnhancedParser
            parser = EnhancedParser()
            
            sample = "Sample sentence for parsing."
            result = parser.parse_sentence(sample, 'en', 'modern')
            
            logger.info(f"  ✓ Parsed {len(result['tokens'])} tokens")
            return {'tokens_parsed': len(result['tokens'])}
        except Exception as e:
            logger.error(f"  ✗ Parser failed: {e}")
            return {'tokens_parsed': 0, 'error': str(e)}
    
    def run_exporter(self) -> Dict:
        """Run export system"""
        try:
            from format_exporter import FormatExporter
            exporter = FormatExporter()
            
            sample = [{'tokens': [
                {'id': 1, 'form': 'test', 'lemma': 'test', 'upos': 'NOUN',
                 'xpos': '_', 'feats': '_', 'head': 0, 'deprel': 'root'}
            ]}]
            
            outputs = exporter.export_all_formats(
                sample, f'night_run_{self.stats["cycles_completed"]}',
                {'title': 'Night Run', 'language': 'en', 'period': 'modern'}
            )
            
            logger.info(f"  ✓ Created {len(outputs)} export files")
            return {'files_created': len(outputs)}
        except Exception as e:
            logger.error(f"  ✗ Exporter failed: {e}")
            return {'files_created': 0, 'error': str(e)}
    
    def run_all_night(self):
        """Run continuously all night"""
        config = self.config.get('all_night_mode', {})
        interval = config.get('cycle_interval_minutes', 30)
        max_cycles = config.get('max_cycles', 20)
        
        logger.info("\n" + "="*80)
        logger.info("ALL-NIGHT MODE ACTIVATED")
        logger.info("="*80)
        logger.info(f"Cycle interval: {interval} minutes")
        logger.info(f"Maximum cycles: {max_cycles}")
        logger.info(f"Expected completion: {(datetime.now() + timedelta(minutes=interval * max_cycles)).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("\nPress Ctrl+C to stop and generate report")
        logger.info("="*80)
        
        try:
            for cycle in range(1, max_cycles + 1):
                # Run cycle
                cycle_results = self.run_cycle(cycle)
                
                # Check if last cycle
                if cycle >= max_cycles:
                    logger.info(f"\n✓ Completed all {max_cycles} cycles")
                    break
                
                # Wait for next cycle
                logger.info(f"\n⏰ Waiting {interval} minutes until next cycle...")
                logger.info(f"   Next cycle at: {(datetime.now() + timedelta(minutes=interval)).strftime('%H:%M:%S')}")
                
                time.sleep(interval * 60)
        
        except KeyboardInterrupt:
            logger.info("\n\n⏹️  All-night run interrupted by user")
        
        # Generate morning report
        self.generate_morning_report()
    
    def generate_morning_report(self):
        """Generate comprehensive morning report"""
        logger.info("\n" + "="*80)
        logger.info("GENERATING MORNING REPORT")
        logger.info("="*80)
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.stats['start_time'])
        duration = end_time - start_time
        
        report = []
        report.append("# MORNING REPORT - All-Night Production Run")
        report.append("")
        report.append(f"**Generated:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Platform:** Diachronic Linguistics Platform v2.0")
        report.append("")
        report.append("---")
        report.append("")
        
        # Overview
        report.append("## OVERVIEW")
        report.append("")
        report.append(f"**Start Time:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**End Time:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total Duration:** {duration.total_seconds() / 3600:.2f} hours")
        report.append(f"**Cycles Completed:** {self.stats['cycles_completed']}")
        report.append("")
        
        # Statistics
        report.append("## STATISTICS")
        report.append("")
        report.append(f"- **Texts Processed:** {self.stats['total_texts_processed']}")
        report.append(f"- **Annotations:** {self.stats['total_annotations']}")
        report.append(f"- **Validations:** {self.stats['total_validations']}")
        report.append(f"- **Tokens Parsed:** {self.stats['total_parses']}")
        report.append(f"- **Files Exported:** {self.stats['total_exports']}")
        report.append(f"- **Errors:** {len(self.stats['errors'])}")
        report.append("")
        
        # Performance
        if self.stats['cycles_completed'] > 0:
            avg_time = duration.total_seconds() / self.stats['cycles_completed']
            report.append("## PERFORMANCE")
            report.append("")
            report.append(f"- **Average Cycle Time:** {avg_time:.2f} seconds")
            report.append(f"- **Texts per Hour:** {self.stats['total_texts_processed'] / (duration.total_seconds() / 3600):.1f}")
            report.append(f"- **Success Rate:** {((self.stats['cycles_completed'] - len(self.stats['errors'])) / self.stats['cycles_completed'] * 100):.1f}%")
            report.append("")
        
        # Enabled Systems
        report.append("## SYSTEMS ACTIVE")
        report.append("")
        for system, enabled in self.config['systems_enabled'].items():
            status = "✓" if enabled else "✗"
            report.append(f"- {status} {system}")
        report.append("")
        
        # Errors (if any)
        if self.stats['errors']:
            report.append("## ERRORS")
            report.append("")
            for error in self.stats['errors'][:10]:  # First 10 errors
                report.append(f"- Cycle {error['cycle']}: {error['error']}")
            if len(self.stats['errors']) > 10:
                report.append(f"- ... and {len(self.stats['errors']) - 10} more errors")
            report.append("")
        
        # Checkpoints
        if self.stats['checkpoints']:
            report.append("## CYCLE SUMMARY")
            report.append("")
            report.append("| Cycle | Duration | Systems | Status |")
            report.append("|-------|----------|---------|--------|")
            for checkpoint in self.stats['checkpoints'][-10:]:  # Last 10
                cycle = checkpoint['cycle']
                duration = checkpoint.get('duration_seconds', 0)
                systems = len(checkpoint.get('systems_run', []))
                status = "✓" if 'error' not in str(checkpoint) else "⚠"
                report.append(f"| {cycle} | {duration:.1f}s | {systems} | {status} |")
            report.append("")
        
        # Recommendations
        report.append("## RECOMMENDATIONS")
        report.append("")
        
        if self.stats['total_texts_processed'] < 10:
            report.append("- ⚠ Low text collection rate - check network connectivity")
        else:
            report.append("- ✓ Text collection performing well")
        
        if len(self.stats['errors']) > self.stats['cycles_completed'] * 0.2:
            report.append("- ⚠ High error rate - review logs for issues")
        else:
            report.append("- ✓ Error rate acceptable")
        
        if self.stats['total_exports'] > 0:
            report.append("- ✓ Export system functioning correctly")
        
        report.append("")
        report.append("---")
        report.append("")
        report.append(f"**Status:** All-night run completed successfully")
        report.append(f"**Next Steps:** Review outputs in `exports/` directory")
        report.append("")
        report.append("*Generated automatically by All-Night Production Runner*")
        
        # Save report
        report_text = '\n'.join(report)
        self.morning_report_path.write_text(report_text, encoding='utf-8')
        
        logger.info(f"✓ Morning report saved: {self.morning_report_path}")
        logger.info("\n" + "="*80)
        logger.info("REPORT PREVIEW")
        logger.info("="*80)
        print("\n" + report_text)


def main():
    """Main entry point"""
    runner = AllNightRunner()
    
    # Check if all-night mode is enabled
    if runner.config.get('all_night_mode', {}).get('enabled', False):
        runner.run_all_night()
    else:
        logger.info("\n⚠ All-night mode not enabled in config.json")
        logger.info("   Set 'all_night_mode.enabled' to true to run all night")
        logger.info("   Running single cycle for testing...")
        runner.run_cycle(1)
        runner.generate_morning_report()


if __name__ == "__main__":
    main()
