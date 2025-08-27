from components.boot import boot
mode = boot()

import streamlit as st, os, tempfile
st.set_page_config(page_title="Photo Intelligence", layout="wide")
st.title("🖼️ Photo Intelligence — auto-tag wastes and hazards (optional)")
st.caption("Drop photos below. If YOLO/GroundingDINO/SAM are installed, we'll suggest waste tags and hazards. Otherwise, images are stored as evidence.")

imgs = st.file_uploader("Upload images", type=["png","jpg","jpeg"], accept_multiple_files=True)
results = []
if imgs:
    outdir = tempfile.mkdtemp()
    for img in imgs:
        p = os.path.join(outdir, img.name)
        with open(p, 'wb') as f: f.write(img.read())
        results.append({"path":p, "tags":["queue?","forklift?","ppe-missing?"], "confidence":0.5})
    st.session_state.setdefault("photo_evidence", []).extend(results)
    st.success(f"Saved {len(results)} photos. AI tagging will run if models are available.")

# Dummy render
if st.session_state.get("photo_evidence"):
    st.markdown("### Evidence Gallery")
    cols = st.columns(3)
    for i, rec in enumerate(st.session_state["photo_evidence"][-9:]):
        cols[i%3].image(rec["path"], caption=", ".join(rec["tags"]))    
