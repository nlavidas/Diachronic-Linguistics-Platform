import streamlit as st
import subprocess
from pathlib import Path

# --- Page Configuration & Setup ---
st.set_page_config(page_title="Platform Control", page_icon="🎮", layout="wide")

st.title("🎮 Platform Control Panel")
st.markdown("Run and manage agents, sync data, and perform maintenance tasks.")

project_root = Path(__file__).resolve().parent.parent.parent

# --- Helper Functions ---
def run_command_in_new_window(command):
    """Runs a command in a new PowerShell window."""
    full_command = f'start powershell -NoExit -Command "{command}"'
    subprocess.Popen(full_command, shell=True)

# --- Control Panel UI ---
st.header("Agent Control")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Launch 24/7 Super Agent", use_container_width=True):
        st.info("Attempting to launch the Super Agent in a new terminal window...")
        python_executable = str(project_root / "venv" / "Scripts" / "python.exe")
        agent_script = str(project_root / "scripts" / "super_agent.py")
        # Command to activate venv and then run the script
        agent_command = f"cd '{project_root}'; .\\venv\\Scripts\\Activate.ps1; python '{agent_script}'; pause"
        run_command_in_new_window(agent_command)
        st.success("Launch command issued. A new PowerShell window should have opened to run the agent.")

with col2:
    if st.button("🛑 Stop All Agents (Force)", use_container_width=True, type="primary"):
        st.warning("Attempting to forcefully stop all Python processes...")
        # This is a powerful command and should be used with care
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"])
        st.success("Stop command issued. All Python agents should be terminated.")

st.divider()

st.header("Project Management")
col1, col2 = st.columns(2)

with col1:
    if st.button("🐙 Sync Project to GitHub", use_container_width=True):
        st.info("This feature will be implemented in a future version.")

with col2:
    if st.button("🔍 Run Quality Control", use_container_width=True):
        st.info("This feature will be implemented in a future version.")

st.divider()
st.info("More tools and actions, including the integration of your other scripts for deep analysis, will be added here.")