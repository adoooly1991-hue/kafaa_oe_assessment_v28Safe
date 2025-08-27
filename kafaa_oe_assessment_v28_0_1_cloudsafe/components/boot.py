
import streamlit as st, json, pathlib, datetime

def _jsonable(v):
    try:
        json.dumps(v); return True
    except Exception:
        return False

def autosave():
    ws = {k:v for k,v in st.session_state.items() if _jsonable(v)}
    ws_dir = pathlib.Path("workspaces"); ws_dir.mkdir(parents=True, exist_ok=True)
    active = st.session_state.get('active_workspace_name')
    p = ws_dir/(active + '.json') if active else ws_dir/"_autosave.json"
    p.write_text(json.dumps(ws, ensure_ascii=False, indent=2), encoding="utf-8")
    st.session_state["_last_autosave"] = datetime.datetime.now().strftime("%H:%M:%S")

def sidebar_mode():
    st.sidebar.markdown("### Mode")
    mode = st.sidebar.radio("Select mode", ["Author","Reviewer"], index=0, key="app_mode")
    # lightweight footer
    st.sidebar.caption(f"Auto-saved at {st.session_state.get('_last_autosave','—')}")
    return mode

def boot():
    mode = sidebar_mode()
    autosave()
    return mode
