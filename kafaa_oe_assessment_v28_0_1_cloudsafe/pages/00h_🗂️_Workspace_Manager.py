from components.boot import boot
mode = boot()

import streamlit as st, json, pathlib, shutil, io, datetime

st.set_page_config(page_title="Workspace Manager", layout="wide")
st.title("🗂️ Workspace Manager")

WS_DIR = pathlib.Path("workspaces"); WS_DIR.mkdir(exist_ok=True, parents=True)
ARCH = WS_DIR/"_archive"; ARCH.mkdir(exist_ok=True, parents=True)

def _jsonable(value):
    try:
        json.dumps(value); return True
    except Exception:
        return False

def _snapshot_state():
    # Keep only jsonable entries
    snap = {k:v for k,v in st.session_state.items() if _jsonable(v)}
    snap["_meta"] = {"saved_at": datetime.datetime.now().isoformat(timespec="seconds")}
    return snap

def _write(name, data):
    path = WS_DIR / f"{name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

def _load(name):
    path = WS_DIR / f"{name}.json"
    if not path.exists(): return None
    return json.loads(path.read_text(encoding="utf-8"))

def _apply(data):
    for k,v in data.items():
        if k == "_meta": continue
        st.session_state[k] = v

colA, colB = st.columns(2)

with colA:
    st.subheader("Save current session as…")
    name = st.text_input("Workspace name", st.session_state.get("client_name","workspace"))
    set_active = st.checkbox("Set as active after save", value=True)
    if st.button("💾 Save workspace"):
        snap = _snapshot_state()
        p = _write(name, snap)
        st.success(f"Saved: {p}")
        if set_active:
            st.session_state['active_workspace_name'] = name
            st.toast(f"Active workspace: {name}")

with colB:
    st.subheader("Export current session")
    if st.button("Download JSON"):
        snap = _snapshot_state()
        buf = io.BytesIO(json.dumps(snap, ensure_ascii=False, indent=2).encode("utf-8"))
        st.download_button("Download", data=buf.getvalue(), file_name=f"{name or 'workspace'}.json")

st.markdown("---")

files = sorted([p.stem for p in WS_DIR.glob("*.json")])
sel = st.selectbox("Available workspaces", files, index=files.index(st.session_state.get("last_workspace","")) if st.session_state.get("last_workspace","") in files else 0 if files else None)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📥 Load"):
        if sel:
            data = _load(sel)
            if data:
                _apply(data)
                st.session_state['active_workspace_name'] = sel
                st.session_state["last_workspace"] = sel
                st.success(f"Loaded workspace '{sel}' into session.")
with col2:
    dup = st.text_input("Duplicate as", value=(sel + "_copy") if sel else "")
    if st.button("🧬 Duplicate"):
        if sel and dup:
            data = _load(sel)
            if data:
                _write(dup, data)
                st.success(f"Duplicated '{sel}' → '{dup}'.")
with col3:
    if st.button("📦 Archive"):
        if sel:
            src = WS_DIR/f"{sel}.json"; dst = ARCH/f"{sel}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if src.exists():
                shutil.move(str(src), str(dst)); st.warning(f"Archived to {dst.name}")
with col4:
    if st.button("🗑 Delete"):
        if sel:
            (WS_DIR/f"{sel}.json").unlink(missing_ok=True); st.error(f"Deleted {sel}")

st.markdown("---")
st.subheader("Import workspace from JSON")
up = st.file_uploader("Upload a workspace JSON", type=["json"])
if up and st.button("Import file"):
    try:
        data = json.loads(up.getvalue().decode("utf-8"))
        nm = data.get("client_name", f"workspace_{datetime.datetime.now().strftime('%H%M%S')}")
        _write(nm, data); st.success(f"Imported as {nm}")
    except Exception as e:
        st.error(f"Import error: {e}")
