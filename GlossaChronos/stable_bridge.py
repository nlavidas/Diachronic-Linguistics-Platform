from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime
import sqlite3

# Add path to your pipeline
sys.path.append('Z:\\Diachronic-Linguistics-Platform')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Fix Unicode issues
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max for large texts

# Allow both local and Vercel
CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'])

# Import pipeline with error handling
try:
    from src.pipeline.pipeline import DiachronicPipeline
    pipeline = DiachronicPipeline()
    pipeline_available = True
except Exception as e:
    print(f"Pipeline not available: {e}")
    pipeline_available = False

# Import AI components with error handling
try:
    from linguistic_ai_engine import LinguisticAIEngine
    from text_classifier import LinguisticClassifier
    from translation_comparer import TranslationComparer
    
    ai_engine = LinguisticAIEngine()
    classifier = LinguisticClassifier()
    comparer = TranslationComparer()
    ai_available = True
except Exception as e:
    print(f"AI components not available: {e}")
    ai_available = False

# Initialize feedback database
def init_feedback_db():
    conn = sqlite3.connect('Z:\\GlossaChronos\\feedback.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS corrections
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  original_text TEXT,
                  original_result TEXT,
                  corrected_result TEXT,
                  correction_type TEXT,
                  reviewer_notes TEXT,
                  confidence_score REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  component TEXT,
                  feedback_type TEXT,
                  description TEXT,
                  severity TEXT)''')
    conn.commit()
    conn.close()

init_feedback_db()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'pipeline': pipeline_available,
        'ai_components': ai_available,
        'services': check_services()
    })

@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_text():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Handle different content types and encodings
        if request.content_type and 'application/json' in request.content_type:
            data = request.get_json(force=True)
        else:
            # Try to parse as JSON anyway
            data = json.loads(request.data.decode('utf-8', errors='ignore'))
        
        text = data.get('text', '')
        period = data.get('period', 'modern')
        
        # Limit text size to prevent timeouts
        if len(text) > 50000:
            text = text[:50000] + "... [truncated for processing]"
        
        # Process with error handling
        if pipeline_available:
            try:
                result = pipeline.process_text(text, metadata={'period': period})
                response = {
                    'status': 'success',
                    'pipeline': {
                        'tokens': result['processed']['tokens'][:100],  # Limit response size
                        'sentences': result['processed']['sentences'][:10],
                        'token_count': result['processed']['token_count'],
                        'sentence_count': result['processed']['sentence_count']
                    },
                    'review_id': save_for_review(text, result)  # Save for human review
                }
            except Exception as e:
                response = {
                    'status': 'partial',
                    'error': str(e),
                    'basic_analysis': basic_analysis(text)
                }
        else:
            response = {
                'status': 'fallback',
                'basic_analysis': basic_analysis(text)
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

@app.route('/api/compare-translations', methods=['POST'])
def compare_translations():
    if not ai_available:
        return jsonify({'error': 'AI components not available'}), 503
    
    data = request.json
    translations = data.get('translations', {})
    
    temp_comparer = TranslationComparer()
    for name, text in translations.items():
        temp_comparer.add_translation(name, text)
    
    return jsonify({
        'vocabulary': temp_comparer.compare_vocabulary(),
        'similarities': {
            f"{v1}_vs_{v2}": temp_comparer.semantic_similarity(v1, v2)
            for v1 in translations for v2 in translations if v1 < v2
        }
    })

@app.route('/api/classify-period', methods=['POST'])
def classify_period():
    if not ai_available:
        return jsonify({'error': 'AI components not available'}), 503
    
    text = request.json.get('text', '')
    try:
        result = classifier.classify_period(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-correction', methods=['POST'])
def submit_correction():
    """Human reviewers submit corrections to improve the system"""
    data = request.json
    
    conn = sqlite3.connect('Z:\\GlossaChronos\\feedback.db')
    c = conn.cursor()
    c.execute('''INSERT INTO corrections 
                 (timestamp, original_text, original_result, corrected_result, 
                  correction_type, reviewer_notes, confidence_score)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (datetime.now().isoformat(),
               data.get('original_text', ''),
               json.dumps(data.get('original_result', {})),
               json.dumps(data.get('corrected_result', {})),
               data.get('correction_type', ''),
               data.get('reviewer_notes', ''),
               data.get('confidence_score', 0.5)))
    conn.commit()
    correction_id = c.lastrowid
    conn.close()
    
    # Learn from correction if possible
    if ai_available and data.get('learn_from_correction', False):
        learn_from_feedback(data)
    
    return jsonify({
        'status': 'success',
        'correction_id': correction_id,
        'message': 'Correction saved and will be used to improve the system'
    })

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    """General feedback about system components"""
    data = request.json
    
    conn = sqlite3.connect('Z:\\GlossaChronos\\feedback.db')
    c = conn.cursor()
    c.execute('''INSERT INTO feedback 
                 (timestamp, component, feedback_type, description, severity)
                 VALUES (?, ?, ?, ?, ?)''',
              (datetime.now().isoformat(),
               data.get('component', ''),
               data.get('feedback_type', ''),
               data.get('description', ''),
               data.get('severity', 'medium')))
    conn.commit()
    feedback_id = c.lastrowid
    conn.close()
    
    return jsonify({
        'status': 'success',
        'feedback_id': feedback_id
    })

@app.route('/api/get-review-queue', methods=['GET'])
def get_review_queue():
    """Get items pending human review"""
    conn = sqlite3.connect('Z:\\GlossaChronos\\feedback.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM corrections 
                 WHERE confidence_score < 0.8 
                 ORDER BY timestamp DESC LIMIT 10''')
    items = c.fetchall()
    conn.close()
    
    return jsonify({
        'items': [dict(zip(['id', 'timestamp', 'original_text', 'original_result', 
                           'corrected_result', 'correction_type', 'reviewer_notes', 
                           'confidence_score'], item)) for item in items]
    })

@app.route('/api/export-corrections', methods=['GET'])
def export_corrections():
    """Export all corrections for training"""
    conn = sqlite3.connect('Z:\\GlossaChronos\\feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM corrections')
    corrections = c.fetchall()
    conn.close()
    
    return jsonify({
        'total_corrections': len(corrections),
        'corrections': [dict(zip(['id', 'timestamp', 'original_text', 'original_result', 
                                'corrected_result', 'correction_type', 'reviewer_notes', 
                                'confidence_score'], c)) for c in corrections]
    })

def basic_analysis(text):
    """Fallback analysis when pipeline fails"""
    return {
        'length': len(text),
        'words': len(text.split()),
        'lines': len(text.split('\n')),
        'preview': text[:200] + '...' if len(text) > 200 else text
    }

def check_services():
    """Check which services are available"""
    services = {}
    
    # Check NLP server
    try:
        import requests
        r = requests.get('http://localhost:8000/test', timeout=1)
        services['nlp'] = r.status_code == 200
    except:
        services['nlp'] = False
    
    # Check Ollama
    try:
        import requests
        r = requests.get('http://localhost:11434', timeout=1)
        services['ollama'] = 'Ollama is running' in r.text
    except:
        services['ollama'] = False
    
    return services

def save_for_review(text, result):
    """Save processing results for human review"""
    conn = sqlite3.connect('Z:\\GlossaChronos\\feedback.db')
    c = conn.cursor()
    c.execute('''INSERT INTO corrections 
                 (timestamp, original_text, original_result, corrected_result, 
                  correction_type, reviewer_notes, confidence_score)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (datetime.now().isoformat(),
               text[:1000],  # Save first 1000 chars
               json.dumps(result),
               '{}',  # Empty corrected result
               'pending_review',
               '',
               0.5))  # Medium confidence
    conn.commit()
    review_id = c.lastrowid
    conn.close()
    return review_id

def learn_from_feedback(correction_data):
    """Use corrections to improve the system (placeholder for ML training)"""
    # This is where you'd retrain models or adjust parameters
    # based on human corrections
    pass

@app.errorhandler(500)
def handle_error(e):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'details': str(e)
    }), 500

if __name__ == '__main__':
    print("Starting Stable Bridge Server on port 5000...")
    print("Human review features enabled")
    print("Feedback database at: Z:\\GlossaChronos\\feedback.db")
    app.run(host='0.0.0.0', port=5000, debug=False)