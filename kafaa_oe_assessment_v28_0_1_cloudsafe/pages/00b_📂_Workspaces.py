from components.boot import boot
mode = boot()

import streamlit as st, os, json, time
from components.persist import export_session, import_session

st.set_page_config(page_title="Workspaces", layout="wide")
st.title("📂 Workspaces — save / load client projects")

st.caption("Save your current inputs as a **workspace JSON** under /data, or load an existing one.")

name = st.text_input("Workspace name", value=f"{st.session_state.get('client_name','Client')}_{st.session_state.get('project_name','Project')}")
safe = "".join([c if c.isalnum() or c in "-_." else "_" for c in name]).strip("_")
path = f"data/{safe}.json"

col1, col2, col3 = st.columns(3)
with col1:
    make_default_save = st.checkbox("Make this the default workspace", value=True)
    if st.button("💾 Save workspace"):
        payload = export_session(st.session_state)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        st.success(f"Saved to {path}")
        if make_default_save:
            with open("data/.last_workspace","w",encoding="utf-8") as f2: f2.write(path.split('/')[-1])
            st.toast("Set as default workspace.")
with col2:
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    pick = st.selectbox("Available workspaces", files)
with col3:
    make_default_load = st.checkbox("Set selected as default", value=True)
    if st.button("📥 Load selected"):
        if pick:
            with open(os.path.join("data", pick), "r", encoding="utf-8") as f:
                payload = json.load(f)
            import_session(st.session_state, payload)
            st.success(f"Loaded {pick}")
            if make_default_load:
                with open("data/.last_workspace","w",encoding="utf-8") as f2: f2.write(pick)
                st.toast("Set as default workspace.")
            st.toast("Workspace loaded. Navigate to pages to see values.")
st.info("Note: Vision photos are stored as temporary paths and may not persist across runs on the cloud.")
