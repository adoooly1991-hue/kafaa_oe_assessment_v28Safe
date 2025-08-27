from components.boot import boot
mode = boot()

import streamlit as st, yaml, json, pathlib, shutil

st.set_page_config(page_title="Benchmarks Admin", layout="wide")
st.title("🛠️ Benchmarks Admin")

bm_path = pathlib.Path("benchmarks/industry_profiles.yaml")
if not bm_path.exists():
    st.error("Missing benchmarks/industry_profiles.yaml")
    st.stop()

with open(bm_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f) or {}
profiles = data.get("profiles", {})

names = list(profiles.keys())
sel = st.selectbox("Select profile", names, index=names.index(st.session_state.get("industry_profile","defense_unmanned_systems")) if "defense_unmanned_systems" in names else 0)

st.sidebar.info("Tip: Edit → Save → Set as Active. Version history is stored; you can review diffs and roll back.")

raw = st.text_area("YAML", value=yaml.safe_dump({"profiles": {sel: profiles.get(sel, {})}}, allow_unicode=True, sort_keys=False), height=340)

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save to file"):
        try:
            # merge update back into file
            doc = yaml.safe_load(raw) or {}
            if "profiles" in doc:
                profiles[sel] = doc["profiles"].get(sel, profiles.get(sel,{}))
                data["profiles"] = profiles
                with open(bm_path, "w", encoding="utf-8") as w:
                    yaml.safe_dump(data, w, allow_unicode=True, sort_keys=False)
                st.success("Saved.")
            else:
                st.warning("YAML should contain a top-level 'profiles' key.")
        except Exception as e:
            st.error(f"YAML error: {e}")
with col2:
    if st.button("✅ Set as Active"):
        st.session_state["industry_profile"] = sel
        st.session_state["benchmarks_active"] = profiles.get(sel, {})
        st.success(f"Active profile: {sel}")
        st.json(st.session_state["benchmarks_active"])


st.markdown("---")
st.subheader("Version History")

hist_dir = pathlib.Path("benchmarks/history"); hist_dir.mkdir(parents=True, exist_ok=True)
log_path = hist_dir/"log.json"
log = []
if log_path.exists():
    try:
        log = json.loads(log_path.read_text(encoding="utf-8"))
    except Exception:
        log = []

note = st.text_input("Change note (for history)", value=st.session_state.get("last_bm_note",""))

if st.button("📝 Save version"):
    # snapshot current file to history
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_path = hist_dir/f"{sel}_{ts}.yaml"
    with open(bm_path, "r", encoding="utf-8") as src:
        snap_path.write_text(src.read(), encoding="utf-8")
    entry = {"profile": sel, "ts": ts, "note": note}
    log.append(entry)
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    st.session_state["last_bm_note"] = note
    st.success(f"Saved version {snap_path.name}")

# List history
items = [e for e in log if e.get("profile")==sel]
if items:
    for e in reversed(items[-10:]):
        colx, coly, colz = st.columns([2,5,2])
        with colx:
            st.write(e["ts"])
        with coly:
            st.write(e.get("note","—"))
        with colz:
            fn = hist_dir/f"{sel}_{e['ts']}.yaml"
            if fn.exists():
                if st.button(f"View diff {e['ts']}", key="v"+e["ts"]):
                    current = bm_path.read_text(encoding="utf-8")
                    prev = fn.read_text(encoding="utf-8")
                    import difflib
                    diff = difflib.unified_diff(prev.splitlines(), current.splitlines(), lineterm="")
                    st.code("\n".join(list(diff))[:4000])
                if st.button(f"Revert to {e['ts']}", key="r"+e["ts"]):
                    shutil.copy(str(fn), str(bm_path))
                    st.warning(f"Reverted to {e['ts']}. Click 'Set as Active' to apply.")
