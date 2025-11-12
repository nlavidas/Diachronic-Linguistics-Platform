"""
SYSTEM CONFIGURATION TOOL
Interactive tool to enable/disable platform components
Easy configuration before all-night runs
"""

import json
from pathlib import Path
import sys


class SystemConfigurator:
    """Interactive configuration tool"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self):
        """Load existing config or create default"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """Default configuration"""
        return {
            "system_name": "Diachronic Linguistics Platform v2.0",
            "configuration_version": "1.0",
            "systems_enabled": {
                "text_collector": True,
                "ai_annotator": False,
                "continuous_trainer": False,
                "quality_validator": True,
                "diachronic_analyzer": True,
                "enhanced_parser": True,
                "format_exporter": True,
                "master_orchestrator": True
            },
            "text_collection": {
                "enabled_sources": {
                    "gutenberg": True,
                    "first1kgreek": True,
                    "wikisource": False,
                    "perseus": False,
                    "proiel": True
                },
                "limits": {
                    "gutenberg_limit": 10,
                    "first1k_limit": 10,
                    "wikisource_limit": 5
                }
            },
            "ai_annotation": {
                "preferred_llm": "ollama_local",
                "fallback_enabled": True,
                "cost_limit_per_session": 1.0
            },
            "training": {
                "enabled": False,
                "epochs_per_session": 3,
                "use_gpu": False
            },
            "validation": {
                "minimum_quality_score": 60.0,
                "strict_mode": False
            },
            "all_night_mode": {
                "enabled": False,
                "cycle_interval_minutes": 30,
                "max_cycles": 20,
                "generate_reports": True,
                "save_checkpoints": True
            },
            "logging": {
                "level": "INFO",
                "save_to_file": True,
                "console_output": True
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"\n✓ Configuration saved to {self.config_path}")
    
    def interactive_configure(self):
        """Interactive configuration wizard"""
        print("="*80)
        print("DIACHRONIC LINGUISTICS PLATFORM - CONFIGURATION WIZARD")
        print("="*80)
        print("\nConfigure which systems to run tonight\n")
        
        # Configure main systems
        print("MAIN SYSTEMS:")
        print("-" * 80)
        
        systems = [
            ("text_collector", "Text Collector", "Collect texts from 6 sources"),
            ("ai_annotator", "AI Annotator", "Annotate with GPT-4/Claude/Gemini/Ollama"),
            ("continuous_trainer", "Continuous Trainer", "Train models on gold treebanks"),
            ("quality_validator", "Quality Validator", "5-phase quality validation"),
            ("diachronic_analyzer", "Diachronic Analyzer", "Semantic shift detection"),
            ("enhanced_parser", "Enhanced Parser", "Advanced UD parsing"),
            ("format_exporter", "Format Exporter", "Export to 5 formats"),
            ("master_orchestrator", "Master Orchestrator", "Coordinate all systems")
        ]
        
        for key, name, desc in systems:
            current = self.config['systems_enabled'].get(key, False)
            status = "ENABLED" if current else "DISABLED"
            print(f"\n{name}")
            print(f"  {desc}")
            print(f"  Current: {status}")
            
            response = input(f"  Enable? (y/n/Enter=keep current): ").strip().lower()
            if response == 'y':
                self.config['systems_enabled'][key] = True
            elif response == 'n':
                self.config['systems_enabled'][key] = False
        
        # Configure all-night mode
        print("\n" + "="*80)
        print("ALL-NIGHT MODE CONFIGURATION")
        print("="*80)
        
        response = input("\nEnable all-night mode? (y/n): ").strip().lower()
        self.config['all_night_mode']['enabled'] = (response == 'y')
        
        if self.config['all_night_mode']['enabled']:
            try:
                interval = input("Cycle interval in minutes (default 30): ").strip()
                if interval:
                    self.config['all_night_mode']['cycle_interval_minutes'] = int(interval)
                
                max_cycles = input("Maximum cycles (default 20): ").strip()
                if max_cycles:
                    self.config['all_night_mode']['max_cycles'] = int(max_cycles)
            except ValueError:
                print("⚠ Invalid input, using defaults")
        
        # Save configuration
        self.save_config()
        
        # Summary
        print("\n" + "="*80)
        print("CONFIGURATION SUMMARY")
        print("="*80)
        
        enabled_count = sum(1 for v in self.config['systems_enabled'].values() if v)
        print(f"\nEnabled systems: {enabled_count}/8")
        print("\nSystems that will run:")
        for key, enabled in self.config['systems_enabled'].items():
            if enabled:
                print(f"  ✓ {key}")
        
        if self.config['all_night_mode']['enabled']:
            interval = self.config['all_night_mode']['cycle_interval_minutes']
            cycles = self.config['all_night_mode']['max_cycles']
            hours = (interval * cycles) / 60
            print(f"\nAll-night mode: ENABLED")
            print(f"  Cycle interval: {interval} minutes")
            print(f"  Maximum cycles: {cycles}")
            print(f"  Expected duration: {hours:.1f} hours")
        else:
            print(f"\nAll-night mode: DISABLED (will run single cycle)")
    
    def quick_configure_all_night(self):
        """Quick configuration for all-night run"""
        print("="*80)
        print("QUICK ALL-NIGHT CONFIGURATION")
        print("="*80)
        
        print("\nPreset configurations:")
        print("1. Conservative (safe systems only)")
        print("2. Standard (most systems enabled)")
        print("3. Full Power (all systems enabled)")
        print("4. Custom (interactive)")
        
        choice = input("\nSelect preset (1-4): ").strip()
        
        if choice == '1':
            # Conservative
            self.config['systems_enabled'] = {
                "text_collector": True,
                "ai_annotator": False,
                "continuous_trainer": False,
                "quality_validator": True,
                "diachronic_analyzer": True,
                "enhanced_parser": True,
                "format_exporter": True,
                "master_orchestrator": True
            }
            self.config['all_night_mode']['enabled'] = True
            self.config['all_night_mode']['cycle_interval_minutes'] = 30
            self.config['all_night_mode']['max_cycles'] = 16  # 8 hours
            print("\n✓ Conservative preset selected")
            
        elif choice == '2':
            # Standard
            self.config['systems_enabled'] = {
                "text_collector": True,
                "ai_annotator": True,
                "continuous_trainer": False,
                "quality_validator": True,
                "diachronic_analyzer": True,
                "enhanced_parser": True,
                "format_exporter": True,
                "master_orchestrator": True
            }
            self.config['all_night_mode']['enabled'] = True
            self.config['all_night_mode']['cycle_interval_minutes'] = 30
            self.config['all_night_mode']['max_cycles'] = 16
            print("\n✓ Standard preset selected")
            
        elif choice == '3':
            # Full Power
            self.config['systems_enabled'] = {k: True for k in self.config['systems_enabled']}
            self.config['all_night_mode']['enabled'] = True
            self.config['all_night_mode']['cycle_interval_minutes'] = 45
            self.config['all_night_mode']['max_cycles'] = 10  # ~7.5 hours
            print("\n✓ Full Power preset selected")
            
        elif choice == '4':
            # Custom
            self.interactive_configure()
            return
        else:
            print("\n⚠ Invalid choice, using standard preset")
            choice = '2'
        
        self.save_config()
        self.show_summary()
    
    def show_summary(self):
        """Show configuration summary"""
        print("\n" + "="*80)
        print("FINAL CONFIGURATION")
        print("="*80)
        
        enabled = [k for k, v in self.config['systems_enabled'].items() if v]
        disabled = [k for k, v in self.config['systems_enabled'].items() if not v]
        
        print(f"\n✓ ENABLED ({len(enabled)}):")
        for system in enabled:
            print(f"  • {system}")
        
        if disabled:
            print(f"\n✗ DISABLED ({len(disabled)}):")
            for system in disabled:
                print(f"  • {system}")
        
        if self.config['all_night_mode']['enabled']:
            interval = self.config['all_night_mode']['cycle_interval_minutes']
            cycles = self.config['all_night_mode']['max_cycles']
            hours = (interval * cycles) / 60
            print(f"\n⏰ ALL-NIGHT MODE:")
            print(f"  • Interval: {interval} minutes")
            print(f"  • Cycles: {cycles}")
            print(f"  • Duration: ~{hours:.1f} hours")
        
        print("\n" + "="*80)
        print("Ready to run! Execute:")
        print("  python run_all_night_production.py")
        print("="*80)


def main():
    """Main entry point"""
    configurator = SystemConfigurator()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        configurator.quick_configure_all_night()
    else:
        configurator.interactive_configure()


if __name__ == "__main__":
    main()
