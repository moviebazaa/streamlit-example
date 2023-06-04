import random
import streamlit as st
import pysrt
from translate import Translator

# Function for some random animations
def random_celeb():
    return random.choice([st.balloons()])

# Function to translate .srt file
def translate_srt(srt_file, target_language):
    subs = pysrt.open(srt_file)

    translator = Translator(to_lang=target_language)
    for sub in subs:
        translated_text = translator.translate(sub.text)
        sub.text = translated_text

    translated_filename = f"translated_{srt_file}"
    subs.save(translated_filename, encoding='utf-8')

    return translated_filename

# Streamlit app
def main():
    st.title("SRT File Translator")

    srt_file = st.file_uploader("Upload .srt file", type=".srt")
    if srt_file:
        target_language = st.selectbox("Select Target Language", ["en", "fr", "es"])  # Add more language options if needed

        if st.button("Translate"):
            with st.spinner("Translating..."):
                translated_file = translate_srt(srt_file, target_language)
                st.success("Translation completed!")

            st.download_button("Download Translated File", translated_file, f"translated_{srt_file.name}")

    random_celeb()

if __name__ == '__main__':
    main()
