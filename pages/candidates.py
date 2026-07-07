import streamlit as st
from pages.core.ui import apply_global_style, render_navbar

st.set_page_config(page_title="Candidates", page_icon="👥")
apply_global_style()
render_navbar()

st.title("Candidates")
st.info("List of processed candidate profiles will appear here.")
