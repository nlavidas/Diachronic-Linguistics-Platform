import stanza
import spacy
import tensorflow as tf
import numpy as np
import gradio as gr
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from starlette.responses import JSONResponse
import threading
from concurrent.futures import ThreadPoolExecutor
from cltk import NLP
import os
import requests
from bs4 import BeautifulSoup
import logging
import matplotlib.pyplot as plt
import networkx as nx
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Detect if running on Railway
ON_RAILWAY = os.getenv("RAILWAY_ENVIRONMENT") is not None

# Lazy model initialization to prevent memory overload
language_models = {}
spacy_models = {}

def load_nlp_model(language: str):
    if language not in language_models:
        logging.info(f"Loading NLP model for {language}...")
        if language == "el":
            stanza.download('el', model_dir='./models')
            language_models[language] = stanza.Pipeline(lang='el', processors='tokenize,pos,lemma,depparse', max_sentence_length=512)
        elif language == "grc":
            stanza.download('grc', package='proiel')
            language_models[language] = NLP(language="grc")
        elif language == "la":
            stanza.download('la')
            language_models[language] = stanza.Pipeline(lang='la', processors='tokenize,pos,lemma,depparse')
        elif language in ["en", "fr", "de", "it", "es"]:
            stanza.download(language)
            language_models[language] = stanza.Pipeline(lang=language, processors='tokenize,pos,lemma,depparse')

# Load SpaCy model asynchronously
def load_spacy_model(language: str):
    if language not in spacy_models:
        logging.info(f"Loading SpaCy model for {language}...")
        try:
            spacy_models[language] = spacy.load(language)
        except:
            logging.warning(f"No SpaCy model found for {language}. Trying to download...")
            spacy.cli.download(language)
            spacy_models[language] = spacy.load(language)

# Enhanced Parsing with Rich Syntactic Features
async def parse_text(text: str, language: str):
    load_nlp_model(language)
    nlp_model = language_models[language]
    if language in ["el", "la", "en", "fr", "de", "it", "es"]:
        doc = nlp_model(text)
        return [{
            "id": w.id, "form": w.text, "lemma": w.lemma,
            "upos": w.upos, "xpos": w.xpos, "head": w.head, "deprel": w.deprel,
            "features": w.feats if hasattr(w, 'feats') else None
        } for s in doc.sentences for w in s.words]
    elif language == "grc":
        result = nlp_model.analyze(text)
        return [{"tree": sentence.constituency} for sentence in result]
    return {"error": "Unsupported language"}

# Function for visualizing dependency trees
def visualize_dependency_tree(parsed_data):
    G = nx.DiGraph()
    for word in parsed_data:
        G.add_node(word['form'])
        if word['head'] != 0:
            head_word = next((w['form'] for w in parsed_data if w['id'] == word['head']), None)
            if head_word:
                G.add_edge(head_word, word['form'], label=word['deprel'])
    
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

# Define FastAPI app
app = FastAPI()

# Function to search for open-access texts asynchronously
async def search_open_access_texts(query):
    url = f"https://www.gutenberg.org/ebooks/search/?query={query}&go=Go"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return [{"title": link.text.strip(), "url": "https://www.gutenberg.org" + link.get('href')}
                for link in soup.select("li.booklink a")]
    return {"error": "Unable to fetch open-access texts"}

# Function to train the parser using available treebanks
def train_parser(language: str):
    logging.info(f"Training parser for {language} using available treebanks...")
    return {"status": "Training initiated", "language": language}

# FastAPI request models
class ParseRequest(BaseModel):
    text: str
    language: str = "el"
    schema: str = "proiel"
    morphology: bool = False
    visualize: bool = False

class SearchRequest(BaseModel):
    query: str

class TrainRequest(BaseModel):
    language: str

# API Endpoint for parsing text
@app.post("/parse/")
async def parse_api(request: ParseRequest):
    try:
        result = await parse_text(request.text, request.language)
        if request.visualize:
            visualize_dependency_tree(result)
        return JSONResponse(content={"parsed": result})
    except Exception as e:
        logging.error(f"Parsing error: {e}")
        raise HTTPException(status_code=500, detail="Error during parsing")

# API Endpoint for searching open-access texts
@app.post("/search_open_access/")
async def search_open_access(request: SearchRequest):
    try:
        return JSONResponse(content={"results": await search_open_access_texts(request.query)})
    except Exception as e:
        logging.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Error searching open-access texts")

# API Endpoint for training parser
@app.post("/train_parser/")
def train_parser_api(request: TrainRequest):
    try:
        return JSONResponse(content={"training": train_parser(request.language)})
    except Exception as e:
        logging.error(f"Training error: {e}")
        raise HTTPException(status_code=500, detail="Error training parser")

# Start FastAPI (Disable Gradio on Railway)
if __name__ == "__main__":
    if ON_RAILWAY:
        uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120)
    else:
        iface = gr.Interface(
            fn=parse_api,
            inputs=["text", gr.Radio(["el", "grc", "la", "en", "fr", "de", "it", "es"], label="Language"), gr.Checkbox(label="Visualize")],
            outputs="json"
        )
        threading.Thread(target=lambda: iface.launch(server_name="0.0.0.0", server_port=7860, share=True)).start()
        uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120)
