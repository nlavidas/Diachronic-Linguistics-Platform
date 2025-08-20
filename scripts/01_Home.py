import streamlit as st
import pandas as pd
from pathlib import Path
import json

st.set_page_config(page_title="Diachronic Linguistics Platform", layout="wide")

st.title("🌍 Diachronic Linguistics Platform")
st.markdown("### Open-Access Texts Corpus Management System")

# Display statistics
corpus_path = Path("corpus_texts")
if corpus_path.exists():
    total_files = len(list(corpus_path.rglob("*.txt")))
    st.metric("Total Texts", f"{total_files:,}")
    
    # Show breakdown by language
    col1, col2, col3, col4 = st.columns(4)
    
    greek_files = len(list((corpus_path / "greek_texts").rglob("*.txt"))) if (corpus_path / "greek_texts").exists() else 0
    latin_files = len(list((corpus_path / "latin_texts").rglob("*.txt"))) if (corpus_path / "latin_texts").exists() else 0
    french_files = len(list((corpus_path / "middle_french_texts").rglob("*.txt"))) if (corpus_path / "middle_french_texts").exists() else 0
    english_files = len(list((corpus_path / "english_retranslations").rglob("*.txt"))) if (corpus_path / "english_retranslations").exists() else 0
    
    col1.metric("Greek Texts", greek_files)
    col2.metric("Latin Texts", latin_files)
    col3.metric("Middle French", french_files)
    col4.metric("English", english_files)

st.sidebar.success("Select a page above.")