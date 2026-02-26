mport streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(page_title="Amelia Reader", layout="wide")
st.title("💕 Amelia Reader - Click Any Line")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Amelia")
    video = st.file_uploader("Amelia video (MP4)", type="mp4")
    if video:
        st.video(video, format="video/mp4", loop=True, autoplay=True)

with col2:
    st.subheader("Document")
    pdf = st.file_uploader("Upload PDF", type="pdf")

    if pdf:
        if "sentences" not in st.session_state or st.button("Reload"):
            with st.spinner("Loading..."):
                reader = PdfReader(pdf)
                text = "".join(page.extract_text() or "" for page in reader.pages)
                sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
                st.session_state.sentences = sentences
            st.success(f"{len(sentences)} lines loaded—click one!")

    if "sentences" in st.session_state:
        for i, line in enumerate(st.session_state.sentences):
            if st.button(f"{i+1}. {line[:70]}...", key=f"btn_{i}"):
                st.write("**Speaking:**", line)
                st.components.v1.html(
                    f'<script>speechSynthesis.speak(new SpeechSynthesisUtterance("{line.replace('"', '\\"')}"));</script>',
                    height=0
                )
