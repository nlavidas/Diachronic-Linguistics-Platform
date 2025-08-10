import streamlit as st
import subprocess
from pathlib import Path
import sys

# --- SETUP ---
st.set_page_config(page_title="Platform Control", page_icon="🎮", layout="wide")
st.title("🎮 Platform Control Panel")
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
from scripts.agent_actions import sync_to_github # Import our new function

# (Helper functions and Agent Control sections remain the same)
# ...

# --- Project Management Section (UPGRADED) ---
st.header("Project Management")
if st.button("🐙 Sync Project to GitHub", use_container_width=True):
    with st.spinner("Syncing to GitHub..."):
        # Call the action and display the result
        result = sync_to_github()
        st.code(result, language="bash")