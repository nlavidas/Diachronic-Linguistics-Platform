import os
import stanza
import spacy
import uvicorn
import logging
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from starlette.responses import JSONResponse

# Load environment variables
load_dotenv()

# Get SketchEngine API Key
SKETCHENGINE_API_KEY = os.getenv("SKETCHENGINE_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Load models dynamically
language_models = {}
spacy_models = {}

def load_nlp_model(language: str):
    if language not in language_models:
        logging.info(f"Loading NLP model for {language}...")
        stanza.download(language, model_dir='./models')
        language_models[language] = stanza.Pipeline(lang=language, processors='tokenize,pos,lemma,depparse')

# API Request Models
class ParseRequest(BaseModel):
    text: str
    language: str

class SearchRequest(BaseModel):
    query: str

# Parsing Endpoint
@app.post("/parse/")
def parse_text(request: ParseRequest):
    try:
        load_nlp_model(request.language)
        nlp_model = language_models[request.language]
        doc = nlp_model(request.text)
        return JSONResponse(content={"parsed": [
            {"word": w.text, "lemma": w.lemma, "pos": w.upos} for s in doc.sentences for w in s.words
        ]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing Error: {str(e)}")

# Open Access Text Search
@app.post("/search_open_access/")
def search_open_access(request: SearchRequest):
    try:
        url = f"https://www.gutenberg.org/ebooks/search/?query={request.query}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return JSONResponse(content={"results": [
                {"title": link.text.strip(), "url": "https://www.gutenberg.org" + link.get('href')}
                for link in soup.select("li.booklink a")
            ]})
        return JSONResponse(content={"error": "Unable to fetch texts"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")

# Start API Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
