import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Corpus Explorer", page_icon="🔎", layout="wide")
st.title("🔎 Corpus Explorer")
st.markdown("Select and analyze the contents of the processed texts in the corpus.")

DB_PATH = Path(__file__).resolve().parent.parent.parent / "corpus.db"
if not DB_PATH.exists():
    st.warning("Database not found.")
else:
    conn = sqlite3.connect(DB_PATH)
    processed_texts_df = pd.read_sql_query("SELECT id, filename, language FROM texts", conn)
    st.header("Text Analysis Viewer")
    selected_text_id = st.selectbox("Select a text:", options=processed_texts_df['id'], format_func=lambda x: f"{processed_texts_df.loc[processed_texts_df['id'] == x, 'filename'].iloc[0]} (ID: {x})")
    if selected_text_id:
        token_query = f"SELECT sentence_id, token_id_in_sent, text, lemma, pos, dependency FROM tokens WHERE text_id = {selected_text_id}"
        tokens_df = pd.read_sql_query(token_query, conn)
        st.dataframe(tokens_df, use_container_width=True)
    conn.close()