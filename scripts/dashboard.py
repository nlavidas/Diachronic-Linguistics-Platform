import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(
    page_title="Diachronic Platform Monitor",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Diachronic Linguistics Platform - Fault Tolerant Monitor")

project_root = Path(__file__).resolve().parent.parent

# Create 4 columns for metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    checkpoint_file = project_root / "agent_checkpoint.json"
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        st.metric("✅ Missions Processed", checkpoint.get('mission_count', 0))
        last_update = checkpoint.get('timestamp', 'Unknown')
        st.caption(f"Last: {last_update[:19]}")
    else:
        st.metric("Missions Processed", 0)

with col2:
    db_path = project_root / "corpus.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM texts")
            text_count = cur.fetchone()[0]
            conn.close()
            st.metric("📚 Texts in Corpus", text_count)
        except:
            st.metric("📚 Texts", "Error")
    else:
        st.metric("📚 Texts", 0)

with col3:
    mission_file = project_root / "master_mission.txt"
    if mission_file.exists():
        with open(mission_file, 'r') as f:
            missions = [l for l in f.readlines() if l.strip() and not l.startswith('#')]
        st.metric("📋 Pending Missions", len(missions))
    else:
        st.metric("📋 Pending Missions", 0)

with col4:
    log_file = project_root / "super_agent_fault_tolerant.log"
    if log_file.exists():
        # Check if agent is active (log updated in last 2 minutes)
        import os
        from datetime import datetime, timedelta
        
        mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
        if datetime.now() - mod_time < timedelta(minutes=2):
            st.metric("🤖 Agent Status", "Active", "🟢")
        else:
            st.metric("🤖 Agent Status", "Idle", "🟡")
    else:
        st.metric("🤖 Agent Status", "Offline", "🔴")

# Add mission interface
st.subheader("➕ Add New Mission")
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    mission_type = st.selectbox(
        "Mission Type",
        ["TEST", "HARVEST", "PROCESS", "DISCOVER", "EXTRACT_VALENCY"]
    )

with col2:
    mission_data = st.text_input("Mission Data (optional)")

with col3:
    if st.button("Add Mission", type="primary"):
        mission_str = f"{mission_type}:{mission_data}" if mission_data else mission_type
        with open(mission_file, 'a', encoding='utf-8') as f:
            f.write(f"{mission_str}\n")
        st.success(f"Added: {mission_str}")
        st.rerun()

# Show recent logs
st.subheader("📜 Recent Activity")
if log_file.exists():
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        recent_lines = lines[-30:]  # Last 30 lines
    
    # Color code the logs
    colored_logs = []
    for line in recent_lines:
        if "[ERROR]" in line:
            colored_logs.append(f"🔴 {line.strip()}")
        elif "[WARNING]" in line:
            colored_logs.append(f"🟡 {line.strip()}")
        elif "Mission completed successfully" in line:
            colored_logs.append(f"✅ {line.strip()}")
        else:
            colored_logs.append(line.strip())
    
    st.code('\n'.join(colored_logs), language='log')
else:
    st.info("No logs available yet")

# Auto-refresh
st.button("🔄 Refresh")
