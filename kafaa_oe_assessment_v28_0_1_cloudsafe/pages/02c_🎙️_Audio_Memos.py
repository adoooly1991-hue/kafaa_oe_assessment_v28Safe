from components.boot import boot
mode = boot()

import streamlit as st, tempfile, os
st.set_page_config(page_title="Audio Memos", layout="wide")
st.title("🎙️ Gemba Memos — speech to text (optional)")
st.caption("Upload voice notes (Arabic/English supported). If faster-whisper is installed, we auto-transcribe and add to Observations context.")

au = st.file_uploader("Upload audio", type=["mp3","wav","m4a","aac","flac"])    
if au:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix="_memo."+au.name.split('.')[-1])
    tmp.write(au.read()); tmp.flush()
    text = None
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")
        segments, info = model.transcribe(tmp.name)
        text = " ".join([s.text for s in segments])
        st.success("Transcribed with faster-whisper.")
    except Exception:
        st.warning("faster-whisper not available; storing raw file only.")
    if text:
        st.session_state.setdefault("gemba_memos", []).append(text)
        st.text_area("Transcript", value=text, height=200)
    st.session_state.setdefault("gemba_files", []).append(tmp.name)
    st.info("Memos and transcripts will be used by the Observation co-author.")
