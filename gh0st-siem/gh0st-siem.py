import sys, os
# Ensure both this folder and its parent (project root) are on the module search path
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import duckdb
from enrichment_engine import EnrichmentEngine
from detection_loader import load_detections
from rule_matcher import match_detections
from alert_generator import generate_alerts

st.set_page_config(layout="wide", page_title="gh0st SIEM")

# Paths
LOGS_PATH = os.path.join(SCRIPT_DIR, "logs", "sample_logs.csv")
DETECTIONS_DIR = os.path.join(SCRIPT_DIR, "detections")
# Enrichment now points to CMDB in project root
ASSETS_PATH = os.path.join(PROJECT_ROOT, "gh0st-cmdb", "data", "assets.csv")
USERS_PATH  = os.path.join(PROJECT_ROOT, "gh0st-cmdb", "data", "users.csv")

# Read logs
if os.path.exists(LOGS_PATH):
    logs_df = pd.read_csv(LOGS_PATH)
else:
    logs_df = pd.DataFrame()

# Initialize enrichment engine
engine = EnrichmentEngine(assets_path=ASSETS_PATH, users_path=USERS_PATH)

st.title("🔔 gh0st SIEM")
tabs = st.tabs(["Alerts", "SQL Query", "Detections", "Load Logs", "Enriched Logs"])

# Alerts tab
with tabs[0]:
    st.header("Detected Alerts")
    detections = load_detections(DETECTIONS_DIR)
    if not logs_df.empty and detections:
        alerts = match_detections(logs_df, detections)
        st.dataframe(alerts)
        if st.button("Generate Alerts"):
            generate_alerts(alerts)
            st.success("Alerts generated and saved.")
    else:
        st.info("No logs or detection rules available.")

# SQL Query tab
with tabs[1]:
    st.header("SQL Query Interface")
    query = st.text_area("Enter SQL query:", "SELECT * FROM logs_df LIMIT 10")
    if st.button("Run SQL"):
        try:
            con = duckdb.connect()
            con.register("logs_df", logs_df)
            result = con.execute(query).fetchdf()
            st.dataframe(result)
        except Exception as e:
            st.error(f"Query failed: {e}")

# Detections tab
with tabs[2]:
    st.header("Detection Loader")
    uploaded_rule = st.file_uploader("Upload Detection Rule (YAML)", type=["yaml","yml"])
    if uploaded_rule:
        os.makedirs(DETECTIONS_DIR, exist_ok=True)
        dest = os.path.join(DETECTIONS_DIR, uploaded_rule.name)
        with open(dest, "wb") as f:
            f.write(uploaded_rule.getvalue())
        st.success(f"Saved detection: {uploaded_rule.name}")
    # List existing
    if os.path.isdir(DETECTIONS_DIR):
        st.markdown("**Existing Detections:**")
        for f in os.listdir(DETECTIONS_DIR):
            st.write(f"- {f}")

# Load Logs tab
with tabs[3]:
    st.header("Log Loader")
    uploaded = st.file_uploader("Upload CSV log files", type="csv", accept_multiple_files=True)
    if uploaded:
        log_dir = os.path.join(SCRIPT_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        for file in uploaded:
            path = os.path.join(log_dir, file.name)
            with open(path, "wb") as out:
                out.write(file.getvalue())
        st.success("Logs uploaded successfully.")

# Enriched Logs tab
with tabs[4]:
    st.header("Enriched Logs")
    log_dir = os.path.join(SCRIPT_DIR, "logs")
    if os.path.isdir(log_dir):
        import pandas as pd
        df = pd.concat([pd.read_csv(os.path.join(log_dir, f))
                        for f in os.listdir(log_dir)], ignore_index=True)
        enriched = engine.enrich(df)
        st.dataframe(enriched)
    else:
        st.info("Upload logs to see enrichment.")
