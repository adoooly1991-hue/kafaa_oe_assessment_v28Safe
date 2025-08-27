
import streamlit as st, pathlib, json, time, os
from datetime import datetime
from components.boot import boot
from components.progress import compute_progress

st.set_page_config(page_title="Home — Workspace Gallery", layout="wide")
boot()

st.title("🏠 OE Assessment — Home")
st.caption("Welcome! Pick up where you left off or start a new workspace. Explore the guided tour when in doubt.")

WS = pathlib.Path("workspaces"); WS.mkdir(exist_ok=True, parents=True)
files = sorted([p for p in WS.glob("*.json") if p.name != "_autosave.json"], key=lambda p: p.stat().st_mtime, reverse=True)

colA, colB = st.columns([3,2])
with colA:
    st.subheader("Your workspaces")
    if not files:
        st.info("No saved workspaces yet. Use **Workspace Manager** to save the current session, or click Seed Demo to populate sample data.")
    else:
        for i, p in enumerate(files[:8]):
            with st.container(border=True):
                meta = {}
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    meta = data.get("_meta", {})
                    client = data.get("client_profile",{}).get("name_en") or data.get("client",{}).get("name_en") or data.get("client_name") or p.stem
                except Exception:
                    client = p.stem
                ts = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                st.write(f"**{client}**  
`{p.name}`  
_Last modified: {ts}_")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    if st.button("Open", key=f"open{i}"):
                        # load into session
                        payload = json.loads(p.read_text(encoding="utf-8"))
                        for k,v in payload.items():
                            if k != "_meta": st.session_state[k] = v
                        st.success(f"Loaded {p.name}. Use the Guided Tour to continue.")
                with c2:
                    if st.button("Duplicate", key=f"dup{i}"):
                        new = WS/(p.stem + "_copy.json"); new.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
                        st.toast(f"Duplicated to {new.name}")
                with c3:
                    st.download_button("Export", data=p.read_bytes(), file_name=p.name, key=f"exp{i}")
                with c4:
                    if st.button("Delete", key=f"del{i}"):
                        os.remove(p); st.toast("Deleted. Refresh to update list.")
with colB:
    st.subheader("Quick start")
    st.page_link("pages/00g_🚀_Seed_Demo.py", label="Seed Demo ➜")
    st.page_link("pages/00i_👋_Guided_Tour.py", label="Guided Tour ➜")
    st.page_link("pages/00h_🗂️_Workspace_Manager.py", label="Workspace Manager ➜")
    st.page_link("pages/08a_📤_Export.py", label="Export ➜")
    st.markdown("---")
    overall, _ = compute_progress()
    st.metric("Overall progress", f"{int(overall*100)}%")


st.markdown("---")
st.subheader("Export gallery")
import json
manifest_p = pathlib.Path("exports/manifest.json")
if manifest_p.exists():

if manifest_p.exists():
    man = json.loads(manifest_p.read_text(encoding="utf-8"))
    for wsname, items in man.items():
        st.markdown(f"### {wsname}")
        if isinstance(items, dict):
            items = [items]
        for rec in reversed(items[-5:]):
            with st.container(border=True):
                ts = rec.get("ts","")
                st.caption(ts)
                prev = rec.get("preview")
                if prev and pathlib.Path(prev).exists():
                    st.image(prev, width=360, caption="Report preview")
                colx, coly, colz = st.columns(3)
                with colx:
                    pptx = rec.get("pptx")
                    if pptx and pathlib.Path(pptx).exists():
                        st.download_button("Download PPTX", data=open(pptx,'rb').read(), file_name=pathlib.Path(pptx).name, key=f"d_{wsname}_{ts}")
                with coly:
                    st.page_link("pages/08a_📤_Export.py", label="Re-generate ➜")
                with colz:
                    # Quick refresh preview using latest session
                    if st.button("Refresh preview", key=f"r_{wsname}_{ts}"):
                        # no-op here; previews are refreshed on Export page
                        st.toast("Use Export page → Live preview to refresh using current session.")

else:
    st.info("No exports yet. Generate a full report in Export page to populate this gallery.")
