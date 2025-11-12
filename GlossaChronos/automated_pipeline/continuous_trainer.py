"""
CONTINUOUS TRAINING SYSTEM
Integrated from training_24_7.py
Self-improving NLP models trained on gold treebanks (307MB!)
PyTorch + Transformers + Multi-task Learning
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json
import time
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TreebankDataset(Dataset):
    """Dataset for continuous training on gold-standard treebanks"""
    
    def __init__(self, data: List[Dict], max_length: int = 128):
        self.data = data
        self.max_length = max_length
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return {
            'form': item['form'],
            'lemma': item['lemma'],
            'pos': item['pos'],
            'deprel': item['deprel'],
            'feats': item.get('feats', '_')
        }


class EnhancedNeuralParser(nn.Module):
    """
    Advanced neural parser with multi-task learning
    Integrated from training_24_7.py
    """
    
    def __init__(self, vocab_size: int = 50000, 
                 embedding_dim: int = 768,
                 num_pos_labels: int = 17, 
                 num_dep_labels: int = 42):
        super().__init__()
        
        # Embeddings
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # LSTM encoder
        self.encoder = nn.LSTM(
            embedding_dim, 
            embedding_dim // 2, 
            num_layers=2,
            bidirectional=True,
            batch_first=True,
            dropout=0.3
        )
        
        # Multi-task heads
        self.pos_classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(embedding_dim, embedding_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(embedding_dim // 2, num_pos_labels)
        )
        
        self.dep_classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(embedding_dim, embedding_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(embedding_dim // 2, num_dep_labels)
        )
        
        self.lemma_encoder = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )
    
    def forward(self, input_ids, lengths):
        # Embed
        embedded = self.embedding(input_ids)
        
        # Pack for LSTM
        packed = nn.utils.rnn.pack_padded_sequence(
            embedded, lengths, batch_first=True, enforce_sorted=False
        )
        
        # Encode
        lstm_out, (hidden, cell) = self.encoder(packed)
        
        # Unpack
        unpacked, _ = nn.utils.rnn.pad_packed_sequence(
            lstm_out, batch_first=True
        )
        
        # Pool (mean of sequence)
        pooled = unpacked.mean(dim=1)
        
        # Multi-task outputs
        pos_logits = self.pos_classifier(pooled)
        dep_logits = self.dep_classifier(pooled)
        lemma_features = self.lemma_encoder(pooled)
        
        return {
            'pos_logits': pos_logits,
            'dep_logits': dep_logits,
            'lemma_features': lemma_features
        }


class ContinuousTrainer:
    """
    Continuous training system that improves models from gold treebanks
    Connects to gold_treebanks.db (307MB of gold-standard data!)
    """
    
    def __init__(self, 
                 base_dir: str = "Z:/GlossaChronos/automated_pipeline",
                 gold_db: str = "Z:/GlossaChronos/gold_treebanks.db"):
        self.base_dir = Path(base_dir)
        self.models_dir = self.base_dir / "trained_models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.gold_db = gold_db
        
        # Training configuration
        self.config = {
            'batch_size': 32,
            'learning_rate': 2e-5,
            'epochs': 10,
            'max_length': 128,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'save_every': 2  # Save checkpoint every 2 epochs
        }
        
        # Statistics
        self.stats = {
            'total_epochs': 0,
            'total_samples': 0,
            'current_loss': 0.0,
            'best_accuracy': 0.0,
            'training_history': []
        }
        
        # Vocabulary
        self.vocab = {'<PAD>': 0, '<UNK>': 1}
        self.pos_to_id = {}
        self.dep_to_id = {}
        
        logger.info("="*80)
        logger.info("CONTINUOUS TRAINING SYSTEM")
        logger.info("="*80)
        logger.info(f"Device: {self.config['device']}")
        logger.info(f"Gold treebank DB: {gold_db}")
    
    def load_gold_treebank_data(self, language: str = 'grc', 
                                limit: int = 10000) -> List[Dict]:
        """
        Load gold-standard treebank data from gold_treebanks.db (307MB!)
        """
        logger.info(f"\n[LOADING] Gold treebank data for {language}...")
        
        if not Path(self.gold_db).exists():
            logger.warning(f"Gold treebank DB not found: {self.gold_db}")
            logger.warning("Using mock data for demonstration")
            return self._get_mock_training_data(limit)
        
        try:
            conn = sqlite3.connect(self.gold_db)
            cur = conn.cursor()
            
            # Check available tables
            tables = cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            
            logger.info(f"  Available tables: {[t[0] for t in tables]}")
            
            # Try to load from tokens table
            try:
                data = cur.execute('''
                    SELECT form, lemma, upos, deprel, feats
                    FROM tokens
                    WHERE form IS NOT NULL
                    LIMIT ?
                ''', (limit,)).fetchall()
                
                conn.close()
                
                if data:
                    formatted = [
                        {
                            'form': row[0],
                            'lemma': row[1] or row[0],
                            'pos': row[2] or 'NOUN',
                            'deprel': row[3] or 'dep',
                            'feats': row[4] or '_'
                        }
                        for row in data
                    ]
                    
                    logger.info(f"  ✓ Loaded {len(formatted)} gold tokens")
                    return formatted
            
            except sqlite3.OperationalError:
                conn.close()
                logger.warning("  Tokens table not found in expected format")
        
        except Exception as e:
            logger.error(f"  Error loading gold data: {e}")
        
        # Fallback to mock data
        return self._get_mock_training_data(limit)
    
    def _get_mock_training_data(self, limit: int) -> List[Dict]:
        """Generate mock training data for demonstration"""
        logger.info(f"  Generating {limit} mock training samples...")
        
        words = ['μῆνιν', 'ἄειδε', 'θεὰ', 'Πηληϊάδεω', 'Ἀχιλῆος']
        pos_tags = ['NOUN', 'VERB', 'NOUN', 'NOUN', 'NOUN']
        deprels = ['obj', 'root', 'nsubj', 'nmod', 'nmod']
        
        data = []
        for i in range(min(limit, 100)):
            idx = i % len(words)
            data.append({
                'form': words[idx],
                'lemma': words[idx].lower(),
                'pos': pos_tags[idx],
                'deprel': deprels[idx],
                'feats': '_'
            })
        
        return data
    
    def build_vocabulary(self, data: List[Dict]):
        """Build vocabulary from training data"""
        logger.info("\n[VOCAB] Building vocabulary...")
        
        # Build word vocabulary
        for item in data:
            if item['form'] not in self.vocab:
                self.vocab[item['form']] = len(self.vocab)
        
        # Build POS vocabulary
        for item in data:
            if item['pos'] not in self.pos_to_id:
                self.pos_to_id[item['pos']] = len(self.pos_to_id)
        
        # Build DEP vocabulary
        for item in data:
            if item['deprel'] not in self.dep_to_id:
                self.dep_to_id[item['deprel']] = len(self.dep_to_id)
        
        logger.info(f"  Vocabulary size: {len(self.vocab)}")
        logger.info(f"  POS tags: {len(self.pos_to_id)}")
        logger.info(f"  DEP relations: {len(self.dep_to_id)}")
    
    def train_model(self, language: str = 'grc', epochs: int = 3):
        """
        Train model on gold treebank data
        Continuous self-improvement!
        """
        logger.info("\n" + "="*80)
        logger.info(f"TRAINING MODEL: {language}")
        logger.info("="*80)
        
        # Load gold data
        train_data = self.load_gold_treebank_data(language, limit=10000)
        
        if not train_data:
            logger.error("No training data available!")
            return
        
        # Build vocabulary
        self.build_vocabulary(train_data)
        
        # Create model
        model = EnhancedNeuralParser(
            vocab_size=len(self.vocab),
            num_pos_labels=len(self.pos_to_id),
            num_dep_labels=len(self.dep_to_id)
        )
        
        device = torch.device(self.config['device'])
        model = model.to(device)
        
        # Create dataset
        dataset = TreebankDataset(train_data)
        dataloader = DataLoader(
            dataset, 
            batch_size=self.config['batch_size'],
            shuffle=True
        )
        
        # Optimizer
        optimizer = torch.optim.AdamW(
            model.parameters(), 
            lr=self.config['learning_rate']
        )
        
        # Loss functions
        pos_criterion = nn.CrossEntropyLoss()
        dep_criterion = nn.CrossEntropyLoss()
        
        # Training loop
        logger.info(f"\n[TRAINING] Starting {epochs} epochs...")
        
        for epoch in range(epochs):
            model.train()
            epoch_loss = 0.0
            batches = 0
            
            logger.info(f"\n  Epoch {epoch+1}/{epochs}")
            
            for batch_idx, batch in enumerate(dataloader):
                # Prepare batch (simplified for demo)
                batch_size = len(batch['form'])
                
                # Convert forms to indices
                input_ids = []
                pos_labels = []
                dep_labels = []
                lengths = []
                
                for i in range(batch_size):
                    form = batch['form'][i]
                    pos = batch['pos'][i]
                    deprel = batch['deprel'][i]
                    
                    word_id = self.vocab.get(form, self.vocab['<UNK>'])
                    pos_id = self.pos_to_id.get(pos, 0)
                    dep_id = self.dep_to_id.get(deprel, 0)
                    
                    input_ids.append([word_id])
                    pos_labels.append(pos_id)
                    dep_labels.append(dep_id)
                    lengths.append(1)
                
                # Convert to tensors
                input_ids = torch.tensor(input_ids, dtype=torch.long).to(device)
                pos_labels = torch.tensor(pos_labels, dtype=torch.long).to(device)
                dep_labels = torch.tensor(dep_labels, dtype=torch.long).to(device)
                lengths = torch.tensor(lengths, dtype=torch.long)
                
                # Forward pass
                optimizer.zero_grad()
                outputs = model(input_ids, lengths)
                
                # Calculate losses
                pos_loss = pos_criterion(outputs['pos_logits'], pos_labels)
                dep_loss = dep_criterion(outputs['dep_logits'], dep_labels)
                
                total_loss = pos_loss + dep_loss
                
                # Backward pass
                total_loss.backward()
                optimizer.step()
                
                epoch_loss += total_loss.item()
                batches += 1
                
                if (batch_idx + 1) % 10 == 0:
                    avg_loss = epoch_loss / batches
                    logger.info(f"    Batch {batch_idx+1}: Loss = {avg_loss:.4f}")
            
            # Epoch summary
            avg_epoch_loss = epoch_loss / batches if batches > 0 else 0
            logger.info(f"  ✓ Epoch {epoch+1} complete: Avg Loss = {avg_epoch_loss:.4f}")
            
            self.stats['total_epochs'] += 1
            self.stats['current_loss'] = avg_epoch_loss
            self.stats['training_history'].append({
                'epoch': epoch + 1,
                'loss': avg_epoch_loss,
                'timestamp': datetime.now().isoformat()
            })
            
            # Save checkpoint
            if (epoch + 1) % self.config['save_every'] == 0:
                self.save_model(model, language, epoch + 1)
        
        # Final save
        self.save_model(model, language, epochs)
        
        logger.info("\n" + "="*80)
        logger.info("TRAINING COMPLETE")
        logger.info("="*80)
        logger.info(f"Total epochs: {self.stats['total_epochs']}")
        logger.info(f"Final loss: {self.stats['current_loss']:.4f}")
    
    def save_model(self, model: nn.Module, language: str, epoch: int):
        """Save model checkpoint"""
        checkpoint_path = self.models_dir / f"{language}_model_epoch{epoch}.pt"
        
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'vocab': self.vocab,
            'pos_to_id': self.pos_to_id,
            'dep_to_id': self.dep_to_id,
            'stats': self.stats
        }, checkpoint_path)
        
        logger.info(f"  💾 Saved checkpoint: {checkpoint_path.name}")
    
    def print_stats(self):
        """Print training statistics"""
        print("\n" + "="*80)
        print("CONTINUOUS TRAINING STATISTICS")
        print("="*80)
        print(f"Total epochs: {self.stats['total_epochs']}")
        print(f"Total samples processed: {self.stats['total_samples']}")
        print(f"Current loss: {self.stats['current_loss']:.4f}")
        print(f"Best accuracy: {self.stats['best_accuracy']:.2%}")
        print(f"Training history: {len(self.stats['training_history'])} records")
        print("="*80 + "\n")


if __name__ == "__main__":
    trainer = ContinuousTrainer()
    
    # Train on Ancient Greek
    trainer.train_model('grc', epochs=3)
    
    # Print statistics
    trainer.print_stats()
