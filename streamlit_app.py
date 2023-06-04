import random
import streamlit as st
import pysrt
from translate import Translator
import os
import time

# Function for some random animations
def random_celeb():
    return random.choice([st.balloons()])

# Function to translate .srt file
def translate_srt(srt_file, target_language):
    temp_path = "temp.srt"
    with open(temp_path, "wb") as f:
        f.write(srt_file.getvalue())

    subs = pysrt.open(temp_path)

    total_subs = len(subs)
    translated_subs = 0

    translator = Translator(to_lang=target_language)
    start_time = time.time()
    for sub in subs:
        translated_text = translator.translate(sub.text)
        sub.text = translated_text

        translated_subs += 1
        progress = translated_subs / total_subs
        percentage = int(progress * 100)
        elapsed_time = time.time() - start_time
        speed = translated_subs / elapsed_time

        st.text(f"Progress: {percentage}% | Speed: {speed:.2f} lines/s", key='progress')

    translated_filename = f"translated_{srt_file.name}"
    translated_path = os.path.join(os.getcwd(), translated_filename)

    subs.save(translated_path, encoding='utf-8')

    os.remove(temp_path)

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

            translated_path = os.path.join(os.getcwd(), translated_file)
            st.download_button("Download Translated File", translated_path, f"translated_{srt_file.name}")

    random_celeb()

if __name__ == '__main__':
    main()
