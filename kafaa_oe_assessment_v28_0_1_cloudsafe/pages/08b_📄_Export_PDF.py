from components.boot import boot
mode = boot()

import streamlit as st, io, os, plotly.graph_objects as go, tempfile, pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from components.roi_bridge import rollup_impact, series_to_waterfall_data
st.set_page_config(page_title="Export PDF", layout="wide")
st.title("📄 Export PDF (brand-styled)")
client_logo = st.session_state.get('client_logo_path')
profile = st.session_state.get('profile_key','default')
use_def = st.session_state.get('use_defense_visuals', False)
ACCENT = "#0B3D91" if (use_def and profile.startswith('defense')) else "#117B77"
logo_path = "assets/kafaa_logo.png"
def _watermark(c, W, H):
    try:
        c.saveState()
        if hasattr(c, "setFillAlpha"): c.setFillAlpha(0.06)
        c.drawImage(ImageReader(logo_path), W/2-200, H/2-120, width=400, preserveAspectRatio=True, mask='auto')
        if hasattr(c, "setFillAlpha"): c.setFillAlpha(1.0)
        c.restoreState()
    except Exception: pass
def build_impact_images(state):
    data = rollup_impact(state); imgs = {}; tmpdir = tempfile.mkdtemp()
    def draw(items, title, key):
        if not items: return
        x,y,m = series_to_waterfall_data(items)
        fig = go.Figure(go.Waterfall(x=x, y=y, measure=m))
        fig.update_layout(title=title, height=300, width=520, margin=dict(l=8,r=8,t=30,b=8))
        path = os.path.join(tmpdir, f"{key}.png"); fig.write_image(path); imgs[key] = path
    draw(data.get("savings_items"), "Savings (SAR/yr)", "wf_savings")
    draw(data.get("frozen_cash_items"), "Frozen Cash (SAR)", "wf_frozen")
    draw(data.get("sales_oppty_items"), "Sales Opportunity (SAR/yr)", "wf_sales")
    return imgs
def pick_kpis(ss):
    takt = ss.get("takt_sec")
    if not takt:
        shift = ss.get("shift_sec") or 8*3600; demand = ss.get("demand_per_shift") or None
        if demand: takt = shift/float(demand)
    ct = None
    if ss.get("ct_table"):
        try: ct = max([r.get("ct",0) for r in ss.get("ct_table")])
        except Exception: pass
    if not ct:
        prod = ss.get("coach_mode_results",{}).get("production",{}).get("answers",{}); ct = prod.get("ct_bn")
    prod = ss.get("coach_mode_results",{}).get("production",{}).get("answers",{}); fpy = prod.get("fpy_line")
    inv = ss.get("financials_inventory") or 0; rate = ss.get("carrying_rate_pct") or 25; carrying = inv * (float(rate)/100.0)
    return {"takt": takt, "ct_bn": ct, "fpy": fpy, "carrying": carrying}
if st.button("Generate PDF"):
    buffer = io.BytesIO(); W,H = A4; c = canvas.Canvas(buffer, pagesize=A4)
    _watermark(c, W, H)
    if os.path.exists(logo_path):
        c.drawImage(ImageReader(logo_path), W-150, H-90, width=120, preserveAspectRatio=True, mask='auto')
    if client_logo and os.path.exists(client_logo):
        c.drawImage(ImageReader(client_logo), 40, H-90, width=100, preserveAspectRatio=True, mask='auto')
    c.setFillColor(colors.HexColor(ACCENT)); c.setFont("Helvetica-Bold", 22); c.drawString(160, H-80, "Kafaa OE — Assessment")
    c.setFillColor(colors.black); c.setFont("Helvetica", 12); c.drawString(160, H-105, f"Factory: {st.session_state.get('factory_name','Factory')}   Year: {st.session_state.get('year','')}   Client: {st.session_state.get('client_name','')}   Project: {st.session_state.get('project_name','')}")
    k = pick_kpis(st.session_state); y = H-160
    for label, val in [("Takt (sec)", k.get("takt")), ("Bottleneck CT (sec)", k.get("ct_bn")), ("FPY (%)", k.get("fpy")), ("Carrying Cost (SAR/yr)", k.get("carrying"))]:
        c.setFont("Helvetica-Bold", 12); c.setFillColor(colors.HexColor(ACCENT)); c.rect(40, y-18, 250, 22, fill=1, stroke=0)
        c.setFillColor(colors.white); c.drawString(48, y-3, label); c.setFillColor(colors.black); c.setFont("Helvetica", 12)
        c.drawString(310, y-3, f"{val:.1f}" if isinstance(val,(int,float)) else str(val)); y -= 26
    c.showPage()
    _watermark(c, W, H)\n    c.setFont("Helvetica-Bold", 18); c.setFillColor(colors.HexColor(ACCENT)); c.drawString(40, H-60, "VSM Charter")\n    y = H-90; c.setFont('Helvetica', 12);\n    def line(txt):\n        nonlocal y\n        c.drawString(40, y, txt); y -= 16\n        if y<60: c.showPage(); _watermark(c, W, H); y = H-60\n    champ = st.session_state.get('champion_product'); line(f"Champion Product: {champ or '—'}")\n    crt = st.session_state.get('cost_reduction_target_sar',0); line(f"Cost Reduction Target: {crt:,.0f} SAR")\n    invr = st.session_state.get('inv_reduction_target_sar',0); line(f"Inventory Reduction Target: {invr:,.0f} SAR")\n    quick = st.session_state.get('quick_ratio'); curr = st.session_state.get('current_ratio'); line(f"Quick Ratio: {quick if quick is not None else '—'} | Current Ratio: {curr if curr is not None else '—'}")\n    scope = st.session_state.get('charter_scope',''); obj = st.session_state.get('charter_objectives','');\n    if scope: line('Scope: ' + scope)\n    if obj: line('Objectives: ' + obj)\n    c.showPage(); _watermark(c, W, H)\n    c.setFont("Helvetica-Bold", 18); c.setFillColor(colors.HexColor(ACCENT)); c.drawString(40, H-60, "Observations (summary)")
    c.setFillColor(colors.black); c.setFont("Helvetica", 11); y = H-90
    obs = st.session_state.get("observations", [])
    for o in obs[:6]:
        for line in [f"{o.get('section','')} — {o.get('title','')}", o.get("text","")[:900]]:
            for seg in [line[i:i+110] for i in range(0, len(line), 110)]:
                c.drawString(40, y, seg); y -= 14
                if y < 60: c.showPage(); _watermark(c, W, H); y = H-60
        y -= 8
    c.showPage()
    _watermark(c, W, H)
    imgs = build_impact_images(st.session_state); c.setFont("Helvetica-Bold", 18); c.setFillColor(colors.HexColor(ACCENT)); c.drawString(40, H-60, "Impact")
    y = H-380
    if imgs.get("wf_savings"): c.drawImage(ImageReader(imgs["wf_savings"]), 40, y, width=500, preserveAspectRatio=True, mask='auto')
    y -= 320
    if y < 100: c.showPage(); _watermark(c, W, H); y = H-380
    if imgs.get("wf_frozen"): c.drawImage(ImageReader(imgs["wf_frozen"]), 40, y, width=500, preserveAspectRatio=True, mask='auto'); y -= 320
    if y < 100: c.showPage(); _watermark(c, W, H); y = H-380
    if imgs.get("wf_sales"): c.drawImage(ImageReader(imgs["wf_sales"]), 40, y, width=500, preserveAspectRatio=True, mask='auto')
    c.showPage(); _watermark(c, W, H); c.setFont("Helvetica-Bold", 24); c.setFillColor(colors.HexColor(ACCENT)); c.drawCentredString(W/2, H/2, "Thank you")
    c.save(); fname = f"Kafaa_OE_Assessment_{st.session_state.get('client_name','Client')}_{st.session_state.get('project_name','Project')}.pdf".replace(' ','_')
log("Export PDF", {"file":"pdf"})
    st.download_button("Download PDF", buffer.getvalue(), file_name=fname)
else:
    st.info("Click **Generate PDF** to export a brand-styled PDF with KPIs and waterfalls.")


# Append audit trail page
def pdf_add_audit(c, W, H):
    from reportlab.lib import colors
    c.showPage()
    draw_watermark_header(c, W, H)
    c.setFont("Helvetica-Bold", 18); c.setFillColor(colors.black)
    c.drawString(40, H-140, "Audit Trail")
    y = H-170
    for item in (st.session_state.get("audit_log", [])[-20:]):
        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"{item.get('ts')} — {item.get('event')}")
        y -= 18
        if y < 80: c.showPage(); draw_watermark_header(c, W, H); y = H-140

from components.heatmap_util import generate_and_store_heatmap
_generate_heat = True
try:
    generate_and_store_heatmap()
except Exception:
    pass


def pdf_signoff_acroform(c, W, H):
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    # New page
    c.showPage()
    draw_watermark_header(c, W, H)
    c.setFont("Helvetica-Bold", 18); c.setFillColor(colors.black)
    c.drawString(40, H-140, "Sign-off and Acceptance")
    c.setFont("Helvetica", 12)
    c.drawString(60, H-180, "For Kafaa:")
    c.drawString(W/2+20, H-180, "For Client:")
    # Signature boxes
    c.setStrokeColor(colors.HexColor("#888888"))
    c.rect(60, H-260, 220, 2, fill=1)   # line
    c.rect(W/2+20, H-260, 220, 2, fill=1)
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(60, H-275, "Name / Title / Signature / Date")
    c.drawString(W/2+20, H-275, "Name / Title / Signature / Date")
    # AcroForm: text fields for names/titles/dates
    form = c.acroForm
    form.textfield(name='kafaa_name', tooltip='Kafaa Name', x=60, y=H-320, width=220, height=18, borderWidth=1, borderColor=colors.black, fillColor=None)
    form.textfield(name='kafaa_title', tooltip='Kafaa Title', x=60, y=H-345, width=220, height=18, borderWidth=1, borderColor=colors.black, fillColor=None)
    form.textfield(name='kafaa_date', tooltip='Kafaa Date', x=60, y=H-370, width=220, height=18, borderWidth=1, borderColor=colors.black, fillColor=None)
    form.textfield(name='client_name', tooltip='Client Name', x=W/2+20, y=H-320, width=220, height=18, borderWidth=1, borderColor=colors.black, fillColor=None)
    form.textfield(name='client_title', tooltip='Client Title', x=W/2+20, y=H-345, width=220, height=18, borderWidth=1, borderColor=colors.black, fillColor=None)
    form.textfield(name='client_date', tooltip='Client Date', x=W/2+20, y=H-370, width=220, height=18, borderWidth=1, borderColor=colors.black, fillColor=None)


def pdf_observations_with_evidence(c, W, H):
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    c.showPage(); draw_watermark_header(c, W, H)
    c.setFont("Helvetica-Bold", 18); c.setFillColor(colors.black)
    c.drawString(40, H-140, "Observations")
    obs_list = st.session_state.get("observations")
    if not obs_list:
        ans = st.session_state.get("rag_last_answer") or ""
        obs_list = [ans] if ans else []
    low = st.session_state.get("obs_low_confidence", False)
    y = H-170
    for i, obs in enumerate(obs_list[:4]):
        c.setFont("Helvetica-Bold", 13)
        title = f"Observation {i+1}" + (" — LOW CONFIDENCE" if low else "")
        c.drawString(60, y, title); y -= 16
        c.setFont("Helvetica", 11)
        text = obs if len(obs) < 700 else obs[:690] + "..."
        for line in text.split("\n"):
            c.drawString(60, y, line[:120]); y -= 14
            if y < 140:
                c.showPage(); draw_watermark_header(c, W, H); y = H-140
        # memo excerpts
        mem = st.session_state.get("gemba_memos") or []
        if mem:
            c.setFont("Helvetica-Oblique", 10); c.setFillColor(colors.HexColor("#555555"))
            c.drawString(60, y, "Memos:"); y -= 14
            for m in mem[:2]:
                c.drawString(80, y, ("• " + (m[:110] + "..."))) ; y -= 12
                if y < 140: c.showPage(); draw_watermark_header(c, W, H); y = H-140
            c.setFillColor(colors.black)
        # confidence bar
        try:
            from components.obs_conf import compute_confidence_for_observation
            c = compute_confidence_for_observation(obs)
            total = max(1, c['measured']+c['inferred'])
            m_ratio = c['measured']/total
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.black)
            c.drawString(60, y, f"Confidence: Measured {c['measured']} / Inferred {c['inferred']}")
            y -= 10
            c.setFillColor(colors.HexColor('#d0d4d9')); c.rect(60, y-8, 300, 8, fill=1, stroke=0)
            c.setFillColor(colors.HexColor('#1b9f97')); c.rect(60, y-8, int(300*m_ratio), 8, fill=1, stroke=0)
            y -= 14
        except Exception:
            pass

        # thumbnails
        photos = st.session_state.get("photo_evidence") or []
        px = 60
        for rec in photos[:2]:
            try:
                p = rec.get("path")
                if p and os.path.exists(p):
                    c.drawImage(ImageReader(p), px, y-80, width=120, height=80, preserveAspectRatio=True, mask='auto')
                    px += 140
            except Exception:
                pass
        y -= 90
        if y < 140: c.showPage(); draw_watermark_header(c, W, H); y = H-140
