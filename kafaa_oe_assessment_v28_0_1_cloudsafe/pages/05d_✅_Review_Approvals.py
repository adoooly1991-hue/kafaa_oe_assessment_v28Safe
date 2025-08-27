
import streamlit as st
from components.boot import boot
from components.reviewer import approvals_panel, reviewer_header

st.set_page_config(page_title="Review & Approvals", layout="wide")
mode = boot()
st.title("✅ Review & Approvals")
reviewer_header()
approvals_panel()
