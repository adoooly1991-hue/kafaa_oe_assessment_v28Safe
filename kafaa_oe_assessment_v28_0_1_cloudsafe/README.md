
# Kafaa OE Assessment — v26.4 Full (Brand + KPI mini-cards + Champion summary + PDF watermark)

**What's new vs v26.3**
- KPI **mini-cards on Home** (live Takt, Bottleneck CT, FPY, Carrying Cost).
- PPTX cover shows KPIs **and** a **Champion Product** summary line (margin & sales) pulled from the Product Selection table.
- PDF export now features a **faint Kafaa watermark** on every page.

Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
Enable AI:
Create `.streamlit/secrets.toml` based on `prompts/secrets_example.toml`.


## v26.6 additions
- **Client & Project branding page** (00a): client name, project, logo (used in PPTX/PDF and filenames).
- **Seed demo loader**: pre-fills financials, product table, coach hints, observations, actions, and sample evidence.
- **Financials**: optional **ABC carrying**; computes weighted carrying cost and uses it in Impact.
- **Countermeasures**: **PACE** rollup (Now/Next/Later) against Cost Reduction Target.



## v26.7 additions
- **📂 Workspaces**: save/load client projects to `/data/*.json` (safe session snapshot).
- **Storytelling Home**: donut progress + checklist and a “Continue to next step” CTA.
- **Champion risk flags**: warns if CT>takt, FPY below benchmark, or changeover too high.
- **Defense profile (unmanned)**: stricter FPY/OTD/MTBF benchmarks and notes.


## v26.8 additions
- Sidebar **workspace picker** + **auto-load last workspace** on start.
- **Industry profile selector** on Home; Coach Mode uses it.
- **Assessment Journey guide** on Home in the requested order, with step cards & links.


## v26.9 additions
- Sidebar **Industry profile selector** (with help tooltip). Active profile chip on Home.
- Prebuilt workspace: `data/Serb_Advanced_Industries_Unmanned_Pilot.json` (defense_unmanned profile).


## v26.10 additions
- **Workspaces**: “Make this the default workspace” on Save/Load (writes `data/.last_workspace`).
- **Defense profile aware exports**: PPTX picks `assets/Kafaa_Template_Defense.pptx` when profile starts with `defense*`, and adds a navy accent bar on the cover. PDF headers switch to navy too.
- Included `assets/Kafaa_Template_Defense.pptx` (initially same as base; you can replace with a custom-styled variant later).


## v26.11 additions
- **Defense PPTX master**: `assets/Kafaa_Template_Defense.pptx` (navy cover band; title/content layouts).
- **Defense icon set** in `assets/` (UAV/QMS/Electrical) used on section slides when a defense profile is active.
- Exporter draws a **navy title bar + icon strip** on section slides for defense profiles.


## v26.12 additions
- **Serb PPTX master**: `assets/Serb_Template.pptx` (cover lock-up, section divider, brand tokens slide).
- Exporter automatically picks the Serb master when the **client name contains “Serb”**; otherwise uses Defense or Kafaa master depending on profile.
- Included **serb_logo_placeholder.png** (use your official logo via Client & Project page to override at export).


## v26.13 additions
- **SERB logo** integrated (`assets/serb_logo.png`) and auto-used when client name includes "Serb" (unless you upload a different client logo).
- **PQCDSM motif icons** on defense section slides.
- **Before vs After** PPTX slide (takt/CT, FPY, Turns, Savings coverage).
- **Insights Heatmap** page (03b) that generates an image; exporter includes it if present.
- **Audit Trail**: simple logger and PPTX/PDF slides.


## v26.14 additions
- **Kafaa-first branding** enforced: app UI and default exports use Kafaa master. Client (e.g., SERB) appears as a secondary co-brand mark on exports.
- Export toggle **Use Defense visual accents** (OFF by default). When ON & profile is defense, adds navy band and defense icons; otherwise keeps Kafaa styling.
- New page **09a — SERB Pilot Workspace**: quick loader with snapshot; still Kafaa-branded throughout.


## v26.15 additions
- **Brand Mode** switch on Export pages: **Kafaa / Co-brand / White-label**.
  - *Kafaa*: Kafaa logo only, teal accents; client logo hidden.
  - *Co-brand*: Kafaa primary + client secondary; teal (or navy if Defense visuals enabled).
  - *White-label*: Client-only logo and neutral accents; title changed to “Operational Excellence Report” in PDF.
- Choice is stored in `st.session_state['brand_mode']` so **PDF** and **PPTX** stay consistent.


## v26.16 additions
- **Brand Control Panel** (00c): set **global default** brand mode and a **project override**.
- Exports now use an **effective brand mode** resolver (`brand_util.effective_brand_mode()`).
- **Fixed logo ratio** on co-brand: Kafaa : Client = **1.4 : 1** in both PPTX and PDF.
- Export page shows the effective mode and allows a temporary per-export tweak (writes project override for the session).


## v27.0 — AI Core (Now + Next)
**Now**
- RAG-grounded observation drafting (LlamaIndex if available; graceful fallback) + heuristic ragas-style metrics.
- Auto VSM draw with push/pull lanes (Graphviz) and **takt vs CT** bars (Plotly).
- Audio memos → faster-whisper transcription (optional) → fed into observations.
- Consolidated **Impact Waterfalls** page for Savings / Frozen Cash / Sales Opportunity.

**Next (optional)**
- Photo Intelligence page (YOLOv10 / GroundingDINO / SAM) to tag wastes/hazards and attach thumbnails.
- Process Mining mode (PM4Py) to discover flows from event logs.
- Coach agent scaffolding with deterministic tools (takt, bottleneck, benchmarks, countermeasures).

> All heavy dependencies are **optional** and loaded dynamically. The app runs without them; install what you need from `requirements.txt`.


## v27.1 — RAG admin + confidence gating + evidenced exports
- **RAG Documents** admin page (00d): upload/manage SOPs and rebuild the vector store. Prefers **Qdrant** when `QDRANT_URL` is set; falls back to local or naive store.
- **Observation confidence gating**: a minimum faithfulness threshold (default 0.70) flags drafts as **LOW CONFIDENCE** for exports.
- **PPTX/PDF exports**: each observation slide/page now includes **memo excerpts** and **photo thumbnails** (when available).


## v27.2 — Relevancy Inspector • Confidence bars • Coach trace
- **Relevancy Inspector (00e)**: shows latest RAG draft, top source snippets, and metrics; download a JSON bundle.
- **Per-observation confidence bars**: measured vs inferred bars added to Observations in **PPTX** and **PDF** exports.
- **Coach trace**: new page **05c — Coach — Why these?** with recommendations and explicit “because” reasoning tied to takt/CT, changeover, FPY, and WIP.


## Final Report Engine (English)
Use the new **report engine** to generate a PPTX that mirrors the structured sample report:

```
python report/report_engine.py --payload report/sample_payload.json --blueprint report/blueprint.yaml --out exports/Assessment_Report.pptx --brand kafaa
```

- Customizes logos and cover per **Brand Mode** (Kafaa / Co-brand / White-label)
- Sections: Cover, Agenda, Methodology, Financials, Product Selection, VSM Summary, Waterfalls Trio, ECRS Funnel, Photos, Assumptions, Disclaimer, Sign‑off.
- Charts are rendered to PNG and inserted; template is `assets/Kafaa_Template.pptx`.


## v27.5 — Export polish
- **Completeness Meter** on Export page (percent + list of missing items).
- **Executive Summary** slide (top KPIs, VSM deltas, champion product).
- **Appendix — RAG Grounded** (latest observation draft + top source snippets) with toggle.


## v27.6 — Export review guard + narrative + notes
- **Completeness threshold** on Export (default 75%): blocks generation until filled (or threshold lowered).
- **Executive Summary narrative** auto-authored from Coach metrics (takt/CT, changeover, FPY, top 3 actions).
- **Per-slide notes**: Exec Summary, VSM Summary, and Waterfalls now include rationale in PPTX notes.


## v27.6.1 — SERB workspace • Benchmarks Admin • Seed Demo
- **SERB workspace**: `workspaces/serb_workspace.json` (co‑brand, defense/unmanned defaults).
- **Benchmarks Admin** (00f): edit and activate sector KPI profiles from `benchmarks/industry_profiles.yaml`.
- **Seed Demo** (00g): one‑click seeding for Defense (Unmanned), Metal Fab, and Electronics; plus a button to load the SERB workspace template into the current session.


## v27.7 — Workspace Manager • Benchmarks versioning • Guided Tour
- **Workspace Manager (00h)**: save/load/duplicate/archive/import/export workspaces (JSON snapshots of session state).
- **Benchmarks Admin (00f)**: version history with change notes; view diffs; revert to a previous version.
- **Guided Tour (00i)**: step-by-step progress with quick links and a smart "next step" button.
- **Progress component**: reusable functions to compute overall progress from session state.


## v27.8 — Front‑page gallery • Auto‑save • Reviewer Mode
- **Home — Workspace Gallery (00j)**: thumbnails list, last modified, Open/Duplicate/Export/Delete, and quick links.
- **Auto‑save**: every page run writes `/workspaces/_autosave.json` and shows a timestamp in the sidebar.
- **Reviewer Mode** (sidebar): switches UI tone and enables **Review & Approvals (05d)** with confidence visuals and decision capture.
- **Boot component**: `components/boot.py` is imported in all pages (including `app.py`) to ensure consistent autosave + mode.


## v27.9 — Export thumbnails • Active autosave • Reviewer checklist
- **Export thumbnails**: the Export page writes a PNG preview + `exports/manifest.json`. The Home Gallery lists recent exports with thumbnails and download buttons.
- **Active autosave**: autosaves into the **active workspace** file (or `_autosave.json` if none). Workspace Manager sets the active workspace on save/load.
- **Reviewer Checklist (PDF)**: from Export, create a reviewer-friendly PDF listing observation decisions and signature boxes; optional signature images can be embedded.


## v28.0 — Live preview • Export history • PPTX appendix
- **Live preview** (Export page): refresh a cover-style PNG thumbnail from the current session without re-exporting PPTX.
- **Export history per workspace**: `exports/manifest.json` now keeps the last 5 exports for each workspace (with timestamps). Home Gallery lists the timeline.
- **Append reviewer checklist to PPTX**: toggle on Export page adds an appendix (decisions + signature slide) directly into the PPTX.


## Cloud-safe profile (v28.0.1)
This build ships a slim `requirements.txt` (pure wheels) and `runtime.txt` (`python-3.11.9`) for Streamlit Cloud.
Heavy/optional dependencies (pm4py, qdrant, cv2, torch, llama-index, etc.) are guarded with `try/except` so the app runs even if they aren't installed.
