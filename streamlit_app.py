import random
import streamlit as st
import pysrt
import os
import time
from google.cloud import translate_v2 as translate

# Function for some random animations
def random_celeb():
    return random.choice([st.balloons()])

# Function to translate .srt file
def translate_srt(srt_file, target_language, api_key):
    temp_path = "temp.srt"
    with open(temp_path, "wb") as f:
        f.write(srt_file.getvalue())

    subs = pysrt.open(temp_path)

    total_subs = len(subs)
    translated_subs = 0

    # Initialize Google Translate client
    translator = translate.Client(api_key)

    start_time = time.time()
    progress_text = st.empty()

    for sub in subs:
        # Translate each subtitle text
        result = translator.translate(sub.text, target_language)

        if 'translatedText' in result:
            translated_text = result['translatedText']
            sub.text = translated_text

        translated_subs += 1
        progress = translated_subs / total_subs
        percentage = int(progress * 100)
        elapsed_time = time.time() - start_time
        speed = translated_subs / elapsed_time

        progress_text.write(f"Progress: {percentage}% | Speed: {speed:.2f} lines/s")

    progress_text.write("")  # Add a line break after the progress is complete

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
        target_language = st.selectbox("Select Target Language", ["en", "fr", "ml", "es"])  # Add more language options if needed
        api_key = st.text_input("Enter Google Translate API Key")

        if st.button("Translate"):
            if api_key:
                with st.spinner("Translating..."):
                    translated_file = translate_srt(srt_file, target_language, api_key)
                    st.success("Translation completed!")

                translated_path = os.path.join(os.getcwd(), translated_file)
                st.download_button("Download Translated File", translated_path, f"translated_{srt_file.name}")
            else:
                st.warning("Please enter the Google Translate API Key")

    random_celeb()

if __name__ == '__main__':
    main()
