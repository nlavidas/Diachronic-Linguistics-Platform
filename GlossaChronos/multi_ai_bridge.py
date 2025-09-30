from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
import subprocess
import sys

app = Flask(__name__)
CORS(app, origins=['*'])

# Load config
with open('ai_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

@app.route('/api/multi-analyze', methods=['POST'])
def multi_analyze():
    """Analyze text with multiple AIs"""
    data = request.json
    text = data.get('text', '')[:1000]  # Limit to 1000 chars
    
    results = {}
    
    # Try Ollama (fast, local)
    try:
        result = subprocess.run(
            ['ollama', 'run', 'phi', f"Analyze: {text[:200]}"],
            capture_output=True, text=True, timeout=5
        )
        results['ollama_phi'] = result.stdout
    except:
        results['ollama_phi'] = "Not available"
    
    # Add other AIs here as you set up their APIs
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5002, debug=True)