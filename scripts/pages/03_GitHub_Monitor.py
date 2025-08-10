import streamlit as st
import subprocess
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(page_title="GitHub Monitor", page_icon="🔗", layout="wide")

st.title("🔗 GitHub Project Monitor")
st.markdown("This page displays the live status of your local Git repository and its connection to GitHub.")

# --- Helper Function to Run Git Commands ---
def run_git_command(command):
    """Runs a Git command and returns its output."""
    try:
        # The 'capture_output=True' and 'text=True' arguments are key
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True, # This will raise an error if the command fails
            cwd=project_root # Run the command from the main project directory
        )
        return result.stdout
    except FileNotFoundError:
        return "Error: Git command not found. Is Git installed and in your PATH?"
    except subprocess.CalledProcessError as e:
        return f"Git command failed:\n{e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Main Page Logic ---
project_root = Path(__file__).resolve().parent.parent.parent

st.header("Local Repository Status")
with st.spinner("Fetching Git status..."):
    # Run the 'git status' command and display the output in a code block
    status_output = run_git_command(["git", "status"])
    st.code(status_output, language="bash")

st.header("Recent Project Commits")
with st.spinner("Fetching commit history..."):
    # Run 'git log' to get the last 5 commits and display them
    log_output = run_git_command(["git", "log", "-n", "5", "--pretty=format:%h - %an, %ar : %s"])
    st.code(log_output, language="bash")
    
st.header("Remote Connection (GitHub)")
with st.spinner("Fetching remote URL..."):
    # Run 'git remote -v' to show the connected GitHub repository URL
    remote_output = run_git_command(["git", "remote", "-v"])
    st.code(remote_output, language="bash")