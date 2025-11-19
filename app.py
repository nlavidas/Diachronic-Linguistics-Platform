from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from text_processor import TextProcessor
from search_engine import SearchEngine

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///texts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize processors
text_processor = TextProcessor()
search_engine = SearchEngine()

# Database Models
class TextDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text)
    abstract = db.Column(db.Text)
    full_text = db.Column(db.Text)
    source = db.Column(db.String(200))
    url = db.Column(db.String(500))
    doi = db.Column(db.String(200))
    publication_date = db.Column(db.Date)
    language = db.Column(db.String(50))
    subject_areas = db.Column(db.Text)
    keywords = db.Column(db.Text)
    word_count = db.Column(db.Integer)
    readability_score = db.Column(db.Float)
    processed_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'source': self.source,
            'url': self.url,
            'doi': self.doi,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'language': self.language,
            'subject_areas': self.subject_areas,
            'keywords': self.keywords,
            'word_count': self.word_count,
            'readability_score': self.readability_score,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_texts():
    data = request.get_json()
    
    # Extract search parameters
    query = data.get('query', '')
    subject_areas = data.get('subject_areas', [])
    language = data.get('language', '')
    date_from = data.get('date_from', '')
    date_to = data.get('date_to', '')
    min_word_count = data.get('min_word_count', 0)
    max_word_count = data.get('max_word_count', 0)
    
    try:
        # Search for texts using the search engine
        results = search_engine.search(
            query=query,
            subject_areas=subject_areas,
            language=language,
            date_from=date_from,
            date_to=date_to,
            min_word_count=min_word_count,
            max_word_count=max_word_count
        )
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/save_text', methods=['POST'])
def save_text():
    data = request.get_json()
    
    try:
        # Process the text
        processed_data = text_processor.process_text(data)
        
        # Create new document
        doc = TextDocument(
            title=processed_data['title'],
            authors=processed_data['authors'],
            abstract=processed_data['abstract'],
            full_text=processed_data['full_text'],
            source=processed_data['source'],
            url=processed_data['url'],
            doi=processed_data['doi'],
            publication_date=processed_data['publication_date'],
            language=processed_data['language'],
            subject_areas=processed_data['subject_areas'],
            keywords=processed_data['keywords'],
            word_count=processed_data['word_count'],
            readability_score=processed_data['readability_score'],
            processed_text=processed_data['processed_text']
        )
        
        db.session.add(doc)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'document_id': doc.id,
            'message': 'Text saved successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/texts')
def list_texts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    texts = TextDocument.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('texts.html', texts=texts)

@app.route('/api/texts')
def api_list_texts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    texts = TextDocument.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'texts': [text.to_dict() for text in texts.items],
        'total': texts.total,
        'pages': texts.pages,
        'current_page': texts.page
    })

@app.route('/text/<int:text_id>')
def view_text(text_id):
    text = TextDocument.query.get_or_404(text_id)
    return render_template('text_detail.html', text=text)

@app.route('/api/text/<int:text_id>')
def api_view_text(text_id):
    text = TextDocument.query.get_or_404(text_id)
    return jsonify(text.to_dict())

@app.route('/preprocess/<int:text_id>', methods=['POST'])
def preprocess_text(text_id):
    text = TextDocument.query.get_or_404(text_id)
    
    try:
        # Reprocess the text
        processed_data = text_processor.process_text({
            'title': text.title,
            'abstract': text.abstract,
            'full_text': text.full_text,
            'language': text.language
        })
        
        # Update the text with new processed data
        text.processed_text = processed_data['processed_text']
        text.word_count = processed_data['word_count']
        text.readability_score = processed_data['readability_score']
        text.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Text reprocessed successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)