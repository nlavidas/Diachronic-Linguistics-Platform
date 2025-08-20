import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="Text Analysis Viewer",
    layout="wide"
)

st.title("🔎 Text Analysis Viewer")
st.markdown("Select a text from the database to view its complete linguistic annotation.")

# --- Database Connection ---
# Use a relative path to find the database from the script's location
DB_PATH = Path(__file__).resolve().parent.parent.parent / "corpus.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    if not DB_PATH.exists():
        st.error(f"Database not found at {DB_PATH}. Please run the preprocessor script first.")
        st.stop()
    return sqlite3.connect(DB_PATH)

# --- Main Page Logic ---
conn = get_db_connection()

try:
    # Load the list of processed texts from the database
    processed_texts_df = pd.read_sql_query("SELECT id, filename, language FROM texts", conn)
    
    if processed_texts_df.empty:
        st.warning("No texts have been processed yet. Please run the preprocessor.")
    else:
        # Allow user to select a text to view
        selected_text_id = st.selectbox(
            "Select a processed text:",
            options=processed_texts_df['id'],
            # This function formats the display in the dropdown menu
            format_func=lambda x: f"{processed_texts_df.loc[processed_texts_df['id'] == x, 'filename'].iloc[0]} (ID: {x})"
        )

        if selected_text_id:
            st.subheader(f"Full Token Analysis for Text ID: {selected_text_id}")
            
            # Query for all tokens of the selected text
            query = f"SELECT sentence_id, token_id_in_sent, text, lemma, pos, dependency, head_text, morphology FROM tokens WHERE text_id = {selected_text_id}"
            tokens_df = pd.read_sql_query(query, conn)
            
            if not tokens_df.empty:
                # Display the data in an interactive, searchable table
                st.dataframe(tokens_df)
            else:
                st.warning("No token data found for this text in the database.")

except Exception as e:
    st.error(f"An error occurred while querying the database: {e}")

finally:
    conn.close()