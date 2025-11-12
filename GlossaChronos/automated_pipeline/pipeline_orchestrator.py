"""
24/7 Pipeline Orchestrator
Real implementation for automated continuous processing
"""

import logging
from pathlib import Path
from datetime import datetime
import json
import time
from typing import Dict, List
import schedule
from concurrent.futures import ThreadPoolExecutor, as_completed

from text_collector import TextCollector
from proiel_processor import ProielProcessor
from valency_extractor import ValencyExtractor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """Orchestrate complete 24/7 processing pipeline"""
    
    def __init__(self, base_dir: str = "Z:\\GlossaChronos\\automated_pipeline"):
        self.base_dir = Path(base_dir)
        self.corpus_dir = self.base_dir / "corpus" / "raw"
        self.processed_dir = self.base_dir / "corpus" / "processed"
        self.output_dir = self.base_dir / "output"
        self.logs_dir = self.base_dir / "logs"
        
        # Create directories
        for dir_path in [self.corpus_dir, self.processed_dir, self.output_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.collector = TextCollector(output_dir=str(self.corpus_dir))
        self.processor = ProielProcessor(models_dir=str(self.base_dir / "models"))
        self.extractor = ValencyExtractor()
        
        # Statistics
        self.stats = {
            'texts_collected': 0,
            'texts_processed': 0,
            'texts_failed': 0,
            'tokens_annotated': 0,
            'patterns_extracted': 0,
            'last_collection': None,
            'last_processing': None,
            'start_time': datetime.now()
        }
        
    def collect_texts(self) -> Dict:
        """Run text collection cycle"""
        logger.info("="*60)
        logger.info("STARTING TEXT COLLECTION CYCLE")
        logger.info("="*60)
        
        try:
            results = self.collector.collect_all()
            total = sum(len(texts) for texts in results.values())
            
            self.stats['texts_collected'] += total
            self.stats['last_collection'] = datetime.now().isoformat()
            
            logger.info(f"Collection complete: {total} texts")
            return results
            
        except Exception as e:
            logger.error(f"Collection failed: {e}")
            return {}
    
    def process_pending_texts(self, max_texts: int = 10) -> Dict:
        """Process pending texts"""
        logger.info("="*60)
        logger.info("STARTING PROCESSING CYCLE")
        logger.info("="*60)
        
        # Find unprocessed texts
        pending_files = list(self.corpus_dir.glob("**/*.json"))
        
        if not pending_files:
            logger.info("No pending texts to process")
            return {'processed': 0, 'failed': 0}
        
        logger.info(f"Found {len(pending_files)} pending texts")
        
        # Process in parallel
        results = {'processed': 0, 'failed': 0, 'details': []}
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self._process_single, f): f 
                for f in pending_files[:max_texts]
            }
            
            for future in as_completed(futures):
                file = futures[future]
                try:
                    result = future.result()
                    if result['status'] == 'success':
                        results['processed'] += 1
                        self.stats['tokens_annotated'] += result['token_count']
                    else:
                        results['failed'] += 1
                    results['details'].append(result)
                except Exception as e:
                    logger.error(f"Processing failed for {file}: {e}")
                    results['failed'] += 1
        
        self.stats['texts_processed'] += results['processed']
        self.stats['texts_failed'] += results['failed']
        self.stats['last_processing'] = datetime.now().isoformat()
        
        logger.info(f"Processing complete: {results['processed']} success, {results['failed']} failed")
        return results
    
    def _process_single(self, text_file: Path) -> Dict:
        """Process single text file"""
        logger.info(f"Processing: {text_file.name}")
        
        try:
            # Step 1: Load text
            with open(text_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            text = data.get('text', '')
            language = data.get('language', 'grc')
            
            # Step 2: Lemmatize
            lemmatized = self.processor.lemmatize(text, language)
            
            # Step 3: Parse
            parsed = self.processor.parse_dependencies(lemmatized)
            
            # Step 4: Extract valency
            valency_patterns = self.extractor.extract_from_parsed(parsed)
            
            # Step 5: Convert formats
            conllu = self.processor.to_conllu(lemmatized)
            proiel_xml = self.processor.to_proiel_xml(lemmatized, data)
            
            # Step 6: Save outputs
            base_name = text_file.stem
            output_base = self.processed_dir / base_name
            
            # Save main output
            output_data = {
                'metadata': data,
                'lemmatized': lemmatized,
                'parsed': parsed,
                'valency_patterns': valency_patterns,
                'statistics': {
                    'token_count': sum(len(s['tokens']) for s in lemmatized),
                    'sentence_count': len(lemmatized),
                    'pattern_count': len(valency_patterns)
                },
                'processed_date': datetime.now().isoformat()
            }
            
            with open(f"{output_base}_complete.json", 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            # Save CONLL-U
            with open(f"{output_base}.conllu", 'w', encoding='utf-8') as f:
                f.write(conllu)
            
            # Save PROIEL XML
            with open(f"{output_base}.xml", 'w', encoding='utf-8') as f:
                f.write(proiel_xml)
            
            # Save valency patterns
            if valency_patterns:
                valency_file = self.output_dir / "valency_patterns" / f"{base_name}_valency.json"
                self.extractor.export_patterns(valency_patterns, valency_file)
            
            token_count = sum(len(s['tokens']) for s in lemmatized)
            self.stats['patterns_extracted'] += len(valency_patterns)
            
            logger.info(f"✓ Processed: {text_file.name} ({token_count} tokens, {len(valency_patterns)} patterns)")
            
            return {
                'status': 'success',
                'file': str(text_file),
                'token_count': token_count,
                'pattern_count': len(valency_patterns)
            }
            
        except Exception as e:
            logger.error(f"✗ Failed: {text_file.name} - {e}")
            return {
                'status': 'error',
                'file': str(text_file),
                'error': str(e)
            }
    
    def generate_summary_report(self) -> str:
        """Generate processing summary report"""
        report = []
        report.append("="*60)
        report.append("24/7 PROCESSING PIPELINE SUMMARY")
        report.append("="*60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Running since: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("PROCESSING STATISTICS")
        report.append("-"*60)
        report.append(f"Texts collected:       {self.stats['texts_collected']}")
        report.append(f"Texts processed:       {self.stats['texts_processed']}")
        report.append(f"Texts failed:          {self.stats['texts_failed']}")
        report.append(f"Tokens annotated:      {self.stats['tokens_annotated']:,}")
        report.append(f"Valency patterns:      {self.stats['patterns_extracted']:,}")
        report.append("")
        
        if self.stats['texts_processed'] > 0:
            success_rate = (self.stats['texts_processed'] / 
                          (self.stats['texts_processed'] + self.stats['texts_failed'])) * 100
            report.append(f"Success rate:          {success_rate:.1f}%")
            report.append(f"Avg tokens/text:       {self.stats['tokens_annotated'] / self.stats['texts_processed']:.0f}")
            report.append(f"Avg patterns/text:     {self.stats['patterns_extracted'] / self.stats['texts_processed']:.1f}")
        
        report.append("")
        report.append("LAST OPERATIONS")
        report.append("-"*60)
        report.append(f"Last collection: {self.stats['last_collection'] or 'Never'}")
        report.append(f"Last processing: {self.stats['last_processing'] or 'Never'}")
        report.append("")
        report.append("="*60)
        
        return '\n'.join(report)
    
    def save_stats(self):
        """Save statistics to file"""
        stats_file = self.logs_dir / f"stats_{datetime.now().strftime('%Y%m%d')}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, default=str)
    
    def run_single_cycle(self):
        """Run single processing cycle"""
        logger.info("\n" + "="*60)
        logger.info(f"STARTING PROCESSING CYCLE: {datetime.now()}")
        logger.info("="*60)
        
        # Collect new texts
        collection_results = self.collect_texts()
        
        # Process pending texts
        processing_results = self.process_pending_texts(max_texts=10)
        
        # Generate and save report
        report = self.generate_summary_report()
        print(report)
        
        report_file = self.logs_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save stats
        self.save_stats()
        
        logger.info("Cycle complete")
    
    def run_continuous(self):
        """Run continuous 24/7 processing"""
        logger.info("="*60)
        logger.info("STARTING 24/7 CONTINUOUS PROCESSING")
        logger.info("="*60)
        
        # Schedule jobs
        schedule.every(1).hours.do(self.run_single_cycle)  # Process every hour
        schedule.every().day.at("02:00").do(self.collect_texts)  # Collect daily at 2 AM
        
        # Initial run
        self.run_single_cycle()
        
        # Continuous loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Stopping pipeline...")
            final_report = self.generate_summary_report()
            print(final_report)
            logger.info("Pipeline stopped")


if __name__ == "__main__":
    orchestrator = PipelineOrchestrator()
    
    # Run single cycle for testing
    print("\nRunning single cycle (for testing)...\n")
    orchestrator.run_single_cycle()
    
    # Uncomment to run continuous 24/7
    # orchestrator.run_continuous()
