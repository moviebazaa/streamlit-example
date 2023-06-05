import streamlit as st
from googletrans import Translator
import pysrt
import base64

# Function to translate .srt file
def translate_srt(srt_file, target_language):
    subs = pysrt.open(srt_file)

    translator = Translator()

    for sub in subs:
        translated_text = translator.translate(sub.text, dest=target_language).text
        sub.text = translated_text

    translated_filename = f"translated_{srt_file.filename}"
    translated_path = translated_filename

    subs.save(translated_path, encoding='utf-8')

    return translated_filename, translated_path

# Streamlit app
def main():
    st.title("SRT File Translator")

    srt_file = st.file_uploader("Upload .srt file", type=".srt")
    if srt_file:
        target_language = st.selectbox("Select Target Language", ["en", "fr", "ml", "es"])  # Add more language options if needed

        if st.button("Translate"):
            with st.spinner("Translating..."):
                translated_file, translated_path = translate_srt(srt_file, target_language)
                st.success("Translation completed!")

            download_link = generate_download_link(translated_path)
            st.markdown(download_link, unsafe_allow_html=True)

def generate_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()
    href = f'<a href="data:file/srt;base64,{encoded_file}" download>Download Translated File</a>'
    return href

if __name__ == '__main__':
    main()
