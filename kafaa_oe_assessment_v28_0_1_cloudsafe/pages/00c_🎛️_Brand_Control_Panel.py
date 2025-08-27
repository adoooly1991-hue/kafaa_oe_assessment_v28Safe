from components.boot import boot
mode = boot()

import streamlit as st

st.set_page_config(page_title="Brand Control Panel", layout="wide")
st.title("🎛️ Brand Control Panel")

st.markdown("Use this control panel to set the **global default** brand mode for exports and optionally a **project-specific override**.")

# Global default
st.subheader("Global default")
st.session_state['brand_mode_global'] = st.selectbox(
    "Default Brand Mode for all projects",
    ["Kafaa","Co-brand","White-label"],
    index=["Kafaa","Co-brand","White-label"].index(st.session_state.get('brand_mode_global','Kafaa')),
    help="Fallback used when no project override is set."
)

# Project override
st.subheader("This project override")
ovr = st.checkbox("Use a project-specific brand mode (override global)", value=st.session_state.get('brand_mode_override', False))
st.session_state['brand_mode_override'] = ovr
if ovr:
    st.session_state['brand_mode_project'] = st.selectbox(
        "Project Brand Mode",
        ["Kafaa","Co-brand","White-label"],
        index=["Kafaa","Co-brand","White-label"].index(st.session_state.get('brand_mode_project', st.session_state.get('brand_mode_global','Kafaa'))),
        help="Applied to the current workspace/project only."
    )
st.success("Settings saved in session. Save your workspace to persist across runs.")


st.subheader("Accent color")
st.session_state['accent_token_choice'] = st.selectbox(
    "Accent token",
    ["Auto (by profile)","Kafaa Teal","Defense Navy","Automotive Blue","Electronics Indigo","Pharma Indigo","Food & Beverage Green","Metal Fab Slate","Neutral Slate"],
    index=["Auto (by profile)","Kafaa Teal","Defense Navy","Automotive Blue","Electronics Indigo","Pharma Indigo","Food & Beverage Green","Metal Fab Slate","Neutral Slate"].index(st.session_state.get('accent_token_choice','Auto (by profile)')),
    help="Controls the main accent color used in PDF and drawn bands in PPTX."
)

st.subheader("Preview (Brand QA)")
from components.brand_util import effective_brand_mode, accent_color_hex
bm = effective_brand_mode()
ACC = accent_color_hex()
import tempfile
from PIL import Image, ImageDraw, ImageFont
w,h=800,200
im=Image.new("RGB",(w,h),(255,255,255))
d=ImageDraw.Draw(im)
# header band
d.rectangle([0,0,w,30], fill=ACC)
# logos as blocks
d.rectangle([20,50,220,120], outline=(17,123,119), width=3)  # Kafaa box
if bm=='Co-brand':
    d.rectangle([w-220,50,w-40,120], outline=(170,170,170), width=3)  # client box
elif bm=='White-label':
    d.rectangle([20,50,240,120], outline=(170,170,170), width=3)  # client only left
# labels
try:
    fnt=ImageFont.truetype("DejaVuSans.ttf",16)
except:
    fnt=None
d.text((24,125), f"Mode: {bm} | Accent: {ACC}", fill=(60,60,60), font=fnt)
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png"); im.save(tmp.name)
st.image(tmp.name, caption="Export header preview")


st.subheader("Cover Simulator (side-by-side)")
from components.brand_util import accent_color_hex
ACC = accent_color_hex()

def _draw_cover(mode:str, accent:str):
    w,h=900,260
    im=Image.new("RGB",(w,h),(255,255,255))
    d=ImageDraw.Draw(im)
    # Accent header band
    d.rectangle([0,0,w,26], fill=accent)
    # Kafaa placeholder block (left)
    if mode in ("Kafaa","Co-brand"):
        d.rectangle([22,46,240,130], outline=(17,123,119), width=4)  # Kafaa logo box
        d.text((26,136), "Kafaa", fill=(17,123,119))
    # Client placeholder
    if mode=="Co-brand":
        d.rectangle([w-240,46,w-22,130], outline=(140,140,140), width=3)
        d.text((w-230,136), "Client", fill=(120,120,120))
    elif mode=="White-label":
        d.rectangle([22,46,280,130], outline=(120,120,120), width=3)
        d.text((26,136), "Client", fill=(120,120,120))
    # Title
    try:
        fnt = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
        f2 = ImageFont.truetype("DejaVuSans.ttf", 16)
    except:
        fnt=f2=None
    d.text((28,180), "Operational Excellence Assessment", fill=(30,30,30), font=fnt)
    d.text((28,210), "Value Stream • Charter • Impact", fill=(50,50,50), font=f2)
    return im

c1,c2,c3 = st.columns(3)
with c1: st.image(_draw_cover("Kafaa", ACC), caption="Kafaa mode")
with c2: st.image(_draw_cover("Co-brand", ACC), caption="Co-brand mode")
with c3: st.image(_draw_cover("White-label", ACC), caption="White-label mode")

st.subheader("Accessibility — Contrast Check (WCAG)")
def _hex_to_rgb(h):
    h=h.lstrip("#")
    return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4))
def _rel_lum(rgb):
    def f(c): return (c/12.92) if (c<=0.03928) else (((c+0.055)/1.055)**2.4)
    r,g,b = [f(c) for c in rgb]
    return 0.2126*r + 0.7152*g + 0.0722*b
def _contrast_ratio(h1,h2):
    L1 = _rel_lum(_hex_to_rgb(h1)); L2 = _rel_lum(_hex_to_rgb(h2))
    L1,L2 = (max(L1,L2), min(L1,L2))
    return (L1+0.05)/(L2+0.05)

accent = ACC
ratios = {
    "Accent vs White text": _contrast_ratio(accent, "#FFFFFF"),
    "Accent vs Black text": _contrast_ratio(accent, "#000000"),
    "White on Accent": _contrast_ratio("#FFFFFF", accent),
    "Black on Accent": _contrast_ratio("#000000", accent),
}
def _wcag(r):
    # AA normal >=4.5; AA large >=3.0; AAA normal >=7.0
    return "AAA" if r>=7.0 else ("AA" if r>=4.5 else ("AA Large" if r>=3.0 else "FAIL"))
st.write({k: f"{v:.2f} ({_wcag(v)})" for k,v in ratios.items()})
st.caption("Tip: Prefer the text color that yields **AA** or **AAA**. Adjust your Accent token if needed.")
