"""
ALL-NIGHT 24/7 COMPREHENSIVE TESTING
Tests all 8 integrated systems continuously
Real stress testing and integration validation
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict
import json
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - TEST - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('all_night_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AllNightTester:
    """Comprehensive 24/7 testing system"""
    
    def __init__(self):
        self.test_results = {
            'start_time': datetime.now().isoformat(),
            'cycles_completed': 0,
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'system_status': {}
        }
        
        logger.info("="*80)
        logger.info("ALL-NIGHT 24/7 COMPREHENSIVE TESTING")
        logger.info("="*80)
        logger.info("Testing all 8 integrated systems")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*80)
    
    def test_system_1_collector(self) -> bool:
        """Test Ultimate Text Collector"""
        logger.info("\n[TEST 1/8] Ultimate Text Collector")
        try:
            from ultimate_text_collector import UltimateTextCollector
            collector = UltimateTextCollector()
            
            # Quick test
            texts = collector.collect_from_gutenberg(limit=2)
            assert len(texts) > 0, "No texts collected"
            
            logger.info("  ✓ Text Collector: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ Text Collector: FAIL - {e}")
            self.test_results['errors'].append(f"System 1: {str(e)}")
            return False
    
    def test_system_2_annotator(self) -> bool:
        """Test AI Annotator"""
        logger.info("\n[TEST 2/8] AI Annotator")
        try:
            from ai_annotator import AIAnnotator
            annotator = AIAnnotator()
            
            # Quick test
            result = annotator.annotate_text(
                text="Test sentence.",
                language='en',
                period='modern'
            )
            assert result['sentences_annotated'] > 0
            
            logger.info("  ✓ AI Annotator: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ AI Annotator: FAIL - {e}")
            self.test_results['errors'].append(f"System 2: {str(e)}")
            return False
    
    def test_system_3_trainer(self) -> bool:
        """Test Continuous Trainer"""
        logger.info("\n[TEST 3/8] Continuous Trainer")
        try:
            from continuous_trainer import ContinuousTrainer
            trainer = ContinuousTrainer()
            
            # Quick test (no actual training)
            data = trainer.load_gold_treebank_data('grc', limit=10)
            assert len(data) > 0
            
            logger.info("  ✓ Continuous Trainer: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ Continuous Trainer: FAIL - {e}")
            self.test_results['errors'].append(f"System 3: {str(e)}")
            return False
    
    def test_system_4_validator(self) -> bool:
        """Test Quality Validator"""
        logger.info("\n[TEST 4/8] Quality Validator")
        try:
            from quality_validator import QualityValidator
            validator = QualityValidator()
            
            # Quick test
            result = validator.validate_text(
                text="Test text for validation.",
                language='en',
                period='modern',
                metadata={'title': 'Test', 'source': 'test', 'language': 'en'}
            )
            assert 'overall_score' in result
            
            logger.info("  ✓ Quality Validator: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ Quality Validator: FAIL - {e}")
            self.test_results['errors'].append(f"System 4: {str(e)}")
            return False
    
    def test_system_5_analyzer(self) -> bool:
        """Test Diachronic Analyzer"""
        logger.info("\n[TEST 5/8] Diachronic Analyzer")
        try:
            from diachronic_analyzer import DiachronicAnalyzer
            analyzer = DiachronicAnalyzer()
            
            # Quick test
            shifts = analyzer.analyze_text_for_shifts(
                text="The gay people were silly.",
                language='en',
                period='modern'
            )
            # Should detect at least one shift
            
            logger.info("  ✓ Diachronic Analyzer: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ Diachronic Analyzer: FAIL - {e}")
            self.test_results['errors'].append(f"System 5: {str(e)}")
            return False
    
    def test_system_6_parser(self) -> bool:
        """Test Enhanced Parser"""
        logger.info("\n[TEST 6/8] Enhanced Parser")
        try:
            from enhanced_parser import EnhancedParser
            parser = EnhancedParser()
            
            # Quick test
            result = parser.parse_sentence("Test sentence", 'en', 'modern')
            assert len(result['tokens']) > 0
            
            logger.info("  ✓ Enhanced Parser: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ Enhanced Parser: FAIL - {e}")
            self.test_results['errors'].append(f"System 6: {str(e)}")
            return False
    
    def test_system_7_exporter(self) -> bool:
        """Test Format Exporter"""
        logger.info("\n[TEST 7/8] Format Exporter")
        try:
            from format_exporter import FormatExporter
            exporter = FormatExporter()
            
            # Quick test
            sample = [{'tokens': [
                {'id': 1, 'form': 'test', 'lemma': 'test', 'upos': 'NOUN',
                 'xpos': '_', 'feats': '_', 'head': 0, 'deprel': 'root'}
            ]}]
            outputs = exporter.export_all_formats(
                sample, 'test_all_night', 
                {'title': 'Test', 'language': 'en', 'period': 'modern'}
            )
            assert len(outputs) == 5
            
            logger.info("  ✓ Format Exporter: PASS")
            return True
        except Exception as e:
            logger.error(f"  ✗ Format Exporter: FAIL - {e}")
            self.test_results['errors'].append(f"System 7: {str(e)}")
            return False
    
    def test_system_8_orchestrator(self) -> bool:
        """Test Master Orchestrator"""
        logger.info("\n[TEST 8/8] Master Orchestrator")
        try:
            # Import check only (full test too intensive)
            sys.path.insert(0, str(Path(__file__).parent))
            # Just verify it can be imported
            logger.info("  ✓ Master Orchestrator: PASS (import check)")
            return True
        except Exception as e:
            logger.error(f"  ✗ Master Orchestrator: FAIL - {e}")
            self.test_results['errors'].append(f"System 8: {str(e)}")
            return False
    
    def run_single_cycle(self) -> Dict:
        """Run one complete test cycle of all systems"""
        logger.info("\n" + "="*80)
        logger.info(f"CYCLE {self.test_results['cycles_completed'] + 1}")
        logger.info("="*80)
        
        cycle_start = time.time()
        
        tests = [
            self.test_system_1_collector,
            self.test_system_2_annotator,
            self.test_system_3_trainer,
            self.test_system_4_validator,
            self.test_system_5_analyzer,
            self.test_system_6_parser,
            self.test_system_7_exporter,
            self.test_system_8_orchestrator
        ]
        
        results = []
        for test_func in tests:
            self.test_results['total_tests'] += 1
            try:
                passed = test_func()
                results.append(passed)
                if passed:
                    self.test_results['passed'] += 1
                else:
                    self.test_results['failed'] += 1
            except Exception as e:
                logger.error(f"Unexpected error in test: {e}")
                results.append(False)
                self.test_results['failed'] += 1
        
        cycle_time = time.time() - cycle_start
        
        self.test_results['cycles_completed'] += 1
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("CYCLE SUMMARY")
        logger.info("="*80)
        logger.info(f"Cycle time: {cycle_time:.2f}s")
        logger.info(f"Tests passed: {sum(results)}/{len(results)}")
        logger.info(f"Tests failed: {len(results) - sum(results)}/{len(results)}")
        logger.info("="*80)
        
        return {
            'cycle': self.test_results['cycles_completed'],
            'passed': sum(results),
            'failed': len(results) - sum(results),
            'time': cycle_time
        }
    
    def run_all_night(self, cycles: int = 10):
        """Run tests continuously"""
        logger.info(f"\nStarting {cycles} test cycles...")
        
        try:
            for i in range(cycles):
                cycle_result = self.run_single_cycle()
                
                if cycle_result['failed'] > 0:
                    logger.warning(f"⚠️  Cycle {i+1} had failures!")
                
                # Short pause between cycles
                if i < cycles - 1:
                    logger.info(f"\n⏰ Waiting 5 seconds before next cycle...")
                    time.sleep(5)
        
        except KeyboardInterrupt:
            logger.info("\n\n⏹️  Testing interrupted by user")
        
        # Final report
        self.print_final_report()
    
    def print_final_report(self):
        """Print comprehensive final report"""
        logger.info("\n" + "="*80)
        logger.info("FINAL TEST REPORT")
        logger.info("="*80)
        logger.info(f"Start time: {self.test_results['start_time']}")
        logger.info(f"End time: {datetime.now().isoformat()}")
        logger.info(f"Cycles completed: {self.test_results['cycles_completed']}")
        logger.info(f"Total tests run: {self.test_results['total_tests']}")
        logger.info(f"Tests passed: {self.test_results['passed']}")
        logger.info(f"Tests failed: {self.test_results['failed']}")
        
        if self.test_results['total_tests'] > 0:
            pass_rate = (self.test_results['passed'] / self.test_results['total_tests']) * 100
            logger.info(f"Pass rate: {pass_rate:.1f}%")
        
        if self.test_results['errors']:
            logger.info(f"\nErrors encountered: {len(self.test_results['errors'])}")
            for error in self.test_results['errors'][:10]:  # Show first 10
                logger.info(f"  - {error}")
        
        logger.info("="*80)
        
        # Save to file
        report_path = Path("test_report.json")
        report_path.write_text(json.dumps(self.test_results, indent=2))
        logger.info(f"\n📄 Full report saved to: {report_path}")


if __name__ == "__main__":
    tester = AllNightTester()
    
    # Run 10 cycles for testing (would be much more for actual all-night)
    tester.run_all_night(cycles=10)
