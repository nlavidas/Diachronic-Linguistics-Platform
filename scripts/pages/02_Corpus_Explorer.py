import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Corpus Explorer", page_icon="🔎", layout="wide")
st.title("🔎 Corpus Explorer")
st.markdown("Select and analyze the contents of the processed texts in the corpus.")

DB_PATH = Path(__file__).resolve().parent.parent.parent / "corpus.db"

def get_db_connection():
    if not DB_PATH.exists():
        st.warning("Database not yet created. Please wait for the agent to process files.")
        return None
    return sqlite3.connect(DB_PATH)

conn = get_db_connection()

if conn:
    try:
        processed_texts_df = pd.read_sql_query("SELECT id, filename, language FROM texts", conn)
        
        if processed_texts_df.empty:
            st.warning("No texts have been processed yet.")
        else:
            st.header("Text Analysis Viewer")
            selected_text_id = st.selectbox(
                "Select a processed text:",
                options=processed_texts_df['id'],
                format_func=lambda x: f"{processed_texts_df.loc[processed_texts_df['id'] == x, 'filename'].iloc[0]} (ID: {x})"
            )

            if selected_text_id:
                query = f"SELECT sentence_id, token_id_in_sent, text, lemma, pos, dependency FROM tokens WHERE text_id = {selected_text_id}"
                tokens_df = pd.read_sql_query(query, conn)
                st.dataframe(tokens_df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()