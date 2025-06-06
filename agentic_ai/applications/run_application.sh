#!/bin/bash		
export PYTHONPATH="$(cd "$(dirname "$0")/.."; pwd)"

# Reload backend and frontend automatically when files or the .env change
watchmedo auto-restart --patterns="*.py;*.env" --recursive -- \
    uvicorn agentic_ai.applications.backend:app --host 0.0.0.0 --port 7000 &
watchmedo auto-restart --patterns="*.py;*.env" --recursive -- \
    streamlit run frontend.py --server.runOnSave true
