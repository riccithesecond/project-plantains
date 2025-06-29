import subprocess
import os
import time

# Mapping of app directories to their script names and ports
apps = {
    "gh0st-siem": {"script": "gh0st-siem.py", "port": 8501},
    "gh0st-soar": {"script": "gh0st-soar.py", "port": 8502},
    "gh0st-cmdb": {"script": "gh0st-cmdb.py", "port": 8503},
    "gh0st-wiki": {"script": "gh0st-wiki.py", "port": 8504},
    "gh0st-jira": {"script": "gh0st-jira.py", "port": 8505}
}

# Determine base directory (where this script lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Launching all project-plantains apps...")

for app_dir, info in apps.items():
    script_name = info["script"]
    port = info["port"]
    app_path = os.path.join(BASE_DIR, app_dir)
    script_path = os.path.join(app_path, script_name)
    if os.path.exists(script_path):
        # Change into the app directory and run the Streamlit app
        cmd = f'start cmd /k "cd {app_path} && streamlit run {script_name} --server.address=0.0.0.0 --server.port={port}"'
        subprocess.Popen(cmd, shell=True)
        print(f"Launched {script_name} in {app_dir} on port {port}")
        time.sleep(1)
    else:
        print(f"❌ Script not found: {script_path}")

print("All launch commands issued.")
