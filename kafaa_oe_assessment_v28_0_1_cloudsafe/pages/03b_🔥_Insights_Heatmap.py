from components.boot import boot
mode = boot()

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os, tempfile

st.set_page_config(page_title="Insights Heatmap", layout="wide")
st.title("🔥 Insights Heatmap — where to focus")

# Example matrix from Coach results (stage × waste score 0..3)
# Expect st.session_state['coach_mode_results'] structure; fallback sample
res = st.session_state.get("coach_mode_results") or {}
stages = list(res.keys()) if res else ["Inbound","Production","Outbound"]
wastes = ["Defects","Waiting","Inventory","Transport","Motion","Over-Processing","Over-Production"]
scores = {stage: {w:0 for w in wastes} for stage in stages}
# try to read provided hints
for stage, dat in res.items():
    top = dat.get("top_wastes") or []
    for wname, sev in top[:3]:
        if wname in wastes:
            scores[stage][wname] = min(3, max(1, int(sev)))

# Render heatmap with PIL
cell_w, cell_h = 120, 44
margin_left, margin_top = 180, 80
img_w = margin_left + cell_w*len(wastes) + 20
img_h = margin_top + cell_h*len(stages) + 20
im = Image.new("RGB", (img_w, img_h), (255,255,255))
d = ImageDraw.Draw(im)

# headers
try:
    f_b = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    f = ImageFont.truetype("DejaVuSans.ttf", 14)
except:
    f_b = f = None

# waste headers
for j,w in enumerate(wastes):
    d.text((margin_left + j*cell_w + 10, 40), w, fill=(60,60,60), font=f_b)
# stage labels
for i,s in enumerate(stages):
    d.text((20, margin_top + i*cell_h + 10), s, fill=(30,30,30), font=f_b)
# cells
def color_for(v):
    return [(236,248,245),(255,243,205),(255,214,153),(235,87,87)][v] if v in (0,1,2,3) else (236,248,245)
for i,s in enumerate(stages):
    for j,w in enumerate(wastes):
        v = scores.get(s,{}).get(w,0)
        x0 = margin_left + j*cell_w; y0 = margin_top + i*cell_h
        d.rectangle([x0, y0, x0+cell_w-4, y0+cell_h-4], fill=color_for(v), outline=(220,220,220))
        d.text((x0+cell_w/2-5, y0+10), str(v), fill=(80,80,80), font=f)

tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
im.save(tmp.name)
st.image(tmp.name, caption="Heatmap: 0=ok, 1=mild, 2=moderate, 3=severe")
st.session_state["heatmap_png"] = tmp.name
st.info("This image will be picked by the PPTX export and added as an 'Insights Heatmap' slide.")

from components.heatmap_util import generate_and_store_heatmap
_generate_heat = True
try:
    generate_and_store_heatmap()
except Exception:
    pass
