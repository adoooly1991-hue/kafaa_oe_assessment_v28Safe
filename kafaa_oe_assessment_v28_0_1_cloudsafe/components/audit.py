
import time, streamlit as st
def log(event:str, meta:dict=None):
    log = st.session_state.setdefault("audit_log", [])
    log.append({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "event": event, "meta": meta or {}})
