# Open Access Text Search Web App

A Flask-based web application for searching, storing, and preprocessing open access academic texts from multiple sources.

## Features

- **Multi-source Search**: Search across ArXiv, DOAJ, PubMed, and other open access repositories
- **Text Storage**: Save and manage texts in a SQLite database
- **Text Preprocessing**: Clean, tokenize, and analyze texts using NLTK and spaCy
- **Modern Web Interface**: Responsive Bootstrap-based UI with real-time search
- **Text Analysis**: Word count, readability scores, keyword extraction, and subject area classification

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

3. Set up the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Use the search interface to find texts based on:
   - Search query
   - Subject areas
   - Language
   - Publication date range
   - Word count range

4. Save interesting texts to your collection

5. View and manage saved texts in the "My Texts" section

## API Endpoints

- `GET /` - Main search interface
- `POST /search` - Search for texts
- `POST /save_text` - Save a text to the database
- `GET /texts` - List saved texts
- `GET /text/<id>` - View specific text details
- `POST /preprocess/<id>` - Reprocess a text

## Database Schema

The application uses SQLAlchemy with the following main model:

- **TextDocument**: Stores text metadata, content, and processing results
  - Basic info: title, authors, abstract, full_text
  - Metadata: source, URL, DOI, publication_date, language
  - Analysis: word_count, readability_score, processed_text
  - Classification: subject_areas, keywords

## Text Processing

The text processor performs:
- Text cleaning and normalization
- Tokenization and lemmatization
- Stop word removal
- Keyword extraction
- Subject area classification
- Readability analysis

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Migrate
- **Text Processing**: NLTK, spaCy, textstat
- **Frontend**: Bootstrap 5, JavaScript (Axios)
- **Database**: SQLite (configurable)
- **Search APIs**: ArXiv, DOAJ, PubMed, Crossref

## Configuration

Create a `.env` file with:
```
DATABASE_URL=sqlite:///texts.db
FLASK_ENV=development
FLASK_DEBUG=True
```

## Development

To run in development mode:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

For production deployment, use a WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```