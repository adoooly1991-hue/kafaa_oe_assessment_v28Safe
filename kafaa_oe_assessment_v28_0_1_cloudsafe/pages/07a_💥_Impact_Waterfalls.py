from components.boot import boot
mode = boot()

import streamlit as st
from components.waterfalls import waterfalls_from_state
st.set_page_config(page_title="Impact Waterfalls", layout="wide")
st.title("💥 Impact — Savings / Frozen Cash / Sales Opportunity")
waterfalls_from_state()
