import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Discovery & Curation", page_icon="🛰️", layout="wide")
st.title("🛰️ AI Discovery & Curation")
st.markdown("Review texts found by the Discovery Agent and approve them for harvesting.")

project_root = Path(__file__).resolve().parent.parent.parent
DISCOVERED_URLS_FILE = project_root / "discovered_urls.csv"
APPROVED_TASKS_FILE = project_root / "master_mission.txt"

st.header("Discovered URLs for Review")

if not DISCOVERED_URLS_FILE.exists():
    st.warning("The Discovery Agent has not found any URLs yet. Run `discovery_agent.py` to begin.")
else:
    try:
        df = pd.read_csv(DISCOVERED_URLS_FILE)
        df["Approve"] = False
        df = df[["Approve", "Title", "Snippet", "URL"]]
        
        st.info(f"Found {len(df)} URLs for review. Check the box to approve a text for harvesting.")
        
        edited_df = st.data_editor(df, hide_index=True, use_container_width=True)
        approved_urls = edited_df.loc[edited_df["Approve"] == True]["URL"].tolist()

        if st.button("Add Approved URLs to Super Agent's Mission Queue"):
            if approved_urls:
                with open(APPROVED_TASKS_FILE, 'a', encoding='utf-8') as f:
                    f.write("\n# --- Approved from Curation Platform ---\n")
                    for url in approved_urls:
                        f.write(f"HARVEST_URL:{url}\n")
                st.success(f"Added {len(approved_urls)} new harvest missions to the queue!")
            else:
                st.warning("No URLs were selected for approval.")
    except pd.errors.EmptyDataError:
        st.info("The discovered URLs file is currently empty.")
    except Exception as e:
        st.error(f"An error occurred: {e}")