import streamlit as st
from pypdf import PdfReader
import re
import json

st.set_page_config(page_title="Reader", layout="wide")
st.title("💕 Reader - Click to Speak")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Amelia")
    video = st.file_uploader("Upload Amelia video loop (MP4)", type="mp4")
    if video:
        st.video(video, format="video/mp4", loop=True, autoplay=True)

with col2:
    st.subheader("Your Document")
    pdf = st.file_uploader("Upload PDF", type="pdf")

    if pdf:
        if "sentences" not in st.session_state or st.button("Reload PDF"):
            with st.spinner("Loading..."):
                reader = PdfReader(pdf)
                text = "".join(page.extract_text() or "" for page in reader.pages)
                sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip() and len(s.strip()) > 5]
                st.session_state.sentences = sentences
            st.success(f"✅ Loaded {len(sentences)} sentences — click any one!")

    if "sentences" in st.session_state:
        sentences_json = json.dumps(st.session_state.sentences)

        html_code = f"""
        <style>
            .sentence {{ cursor: pointer; padding: 12px; margin: 8px 0; background: white; border: 2px solid #ff69b4; border-radius: 10px; }}
            .sentence:hover {{ background: #ffebee; }}
        </style>

        <div id="text"></div>

        <script>
            let sentences = {sentences_json};
            let utterance = null;

            function speak(idx) {{
                if (utterance) window.speechSynthesis.cancel();
                utterance = new SpeechSynthesisUtterance(sentences[idx]);
                utterance.rate = 0.95;
                utterance.pitch = 1.2;
                window.speechSynthesis.speak(utterance);
            }}

            let html = '';
            for (let i = 0; i < sentences.length; i++) {{
                html += '<div class="sentence" onclick="speak(' + i + ')">' + (i + 1) + '. ' + sentences[i] + '</div>';
            }}
            document.getElementById('text').innerHTML = html;
        </script>
        """

        st.components.v1.html(html_code, height=700, scrolling=True)
