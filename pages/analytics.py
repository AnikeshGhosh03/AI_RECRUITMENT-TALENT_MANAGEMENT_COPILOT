import streamlit as st
from pages.core.ui import apply_global_style, render_navbar

st.set_page_config(page_title="Analytics", page_icon="📊")
apply_global_style()
render_navbar()

st.title("Analytics")
st.info("Analytics dashboard will be available here.")
