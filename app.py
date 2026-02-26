import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(page_title="Reader", layout="wide")
st.title("Reader - Click to Speak")

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
                text = ""
                for page in reader.pages:
                    text += (page.extract_text() or "") + "\n"
                sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip() and len(s.strip()) > 5]
                st.session_state.sentences = sentences
            st.success(f"{len(sentences)} sentences—click any!")

    if "sentences" in st.session_state:
        for i, sent in enumerate(st.session_state.sentences):
            if st.button(f"{i+1}. {sent[:60]}...", key=f"btn_{i}"):
                st.write("**Speaking:**", sent)
                st.components.v1.html(
                    f'<script>speechSynthesis.speak(new SpeechSynthesisUtterance("{sent.replace('"', '\\"')}"));</script>',
                    height=0
                )
