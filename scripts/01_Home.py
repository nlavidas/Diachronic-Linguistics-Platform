import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Project Dashboard", page_icon="📖", layout="wide")
st.title("📖 Diachronic Linguistics Platform Dashboard")
st.markdown("Live monitor for the project's data harvesting and processing agents.")

DB_PATH = Path(__file__).resolve().parent.parent / "corpus.db"
LOG_PATH = Path(__file__).resolve().parent.parent / "agent_log.txt"

def get_db_connection():
    if not DB_PATH.exists(): return None
    return sqlite3.connect(DB_PATH)

conn = get_db_connection()

if not conn:
    st.warning("Database not yet created. Please wait for the agent to process files.")
else:
    try:
        st.header("Corpus At A Glance")
        text_count = pd.read_sql_query("SELECT COUNT(id) FROM texts", conn).iloc[0, 0]
        lang_count = pd.read_sql_query("SELECT COUNT(DISTINCT language) FROM texts", conn).iloc[0, 0]
        token_count = pd.read_sql_query("SELECT COUNT(id) FROM tokens", conn).iloc[0, 0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Texts Processed", f"{text_count:,}")
        col2.metric("Languages Detected", f"{lang_count:,}")
        col3.metric("Tokens in Database", f"{token_count:,}")
        st.divider()
        st.subheader("Files Processed by Language")
        lang_summary_df = pd.read_sql_query("SELECT language, COUNT(id) as file_count FROM texts GROUP BY language", conn)
        if not lang_summary_df.empty:
            fig = px.bar(lang_summary_df, x='language', y='file_count', title="Corpus Composition", labels={'language': 'Language', 'file_count': 'Number of Files'}, color='language', template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        st.divider()
        st.subheader("Live Agent Log")
        if LOG_PATH.exists():
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                log_lines = f.readlines()
            st.code('\n'.join(log_lines[-20:]), language='log')
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()