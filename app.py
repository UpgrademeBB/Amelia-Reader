import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(page_title="Amelia Reader", layout="wide")
st.title("💕 Amelia Reader - Click Any Sentence")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Amelia")
    video = st.file_uploader("Upload Amelia video loop (MP4)", type="mp4")
    if video:
        st.video(video, format="video/mp4", loop=True, autoplay=True)

with col2:
    st.subheader("Your Document")
    pdf = st.file_uploader("Upload PDF", type="pdf")
