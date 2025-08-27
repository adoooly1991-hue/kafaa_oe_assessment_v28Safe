from components.boot import boot
mode = boot()

import streamlit as st, os, tempfile
from components.ai_client import vision_describe
st.set_page_config(page_title="Vision Tagger", layout="wide")
st.title("🖼️ Vision Waste Tagger")
stage = st.selectbox("Stage", ["Sourcing","Inbound","Warehouse","Internal Logistics","Production","Maintenance","Outbound"], index=4)
label = st.text_input("Short label (e.g., 'WIP before coating')", value="Evidence")
img = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
prompt = st.text_area("Prompt", value="Identify wastes (transportation, waiting, defects, overprocessing, inventory, motion) and safety hazards. Quantify if possible.")
col1,col2 = st.columns(2)
if img and col1.button("Analyze"):
    res = vision_describe(img.read(), prompt); st.success("Done."); st.write(res)
if img and col2.button("Save to evidence"):
    tmpdir = tempfile.mkdtemp(); path = os.path.join(tmpdir, img.name)
    with open(path, "wb") as f: f.write(img.getbuffer())
    store = st.session_state.setdefault("vision_evidence", {}); store.setdefault(stage, []).append({"label": label, "path": path})
    st.success("Saved. This will appear in the PPTX export grid.")
st.markdown("---"); st.subheader("Current evidence")
store = st.session_state.get("vision_evidence", {})
for stg, items in store.items():
    st.write(f"**{stg}**"); cols = st.columns(4)
    for i, it in enumerate(items[:8]):
        with cols[i%4]: st.image(it["path"], caption=it.get("label",""), use_column_width=True)
