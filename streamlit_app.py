import random
import streamlit as st
import pysrt
from google.cloud import translate_v2 as translate
import os
import time
from concurrent import futures
import base64

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

    translator = translate.Client()
    start_time = time.time()
    progress_text = st.empty()

    def translate_line(sub):
        translated_text = translator.translate(sub.text, target_language, source_language='en')
        sub.text = translated_text['translatedText']

    with futures.ThreadPoolExecutor() as executor:
        future_to_sub = {executor.submit(translate_line, sub): sub for sub in subs}
        for future in futures.as_completed(future_to_sub):
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

    return translated_filename, translated_path

# Streamlit app
def main():
    st.title("SRT File Translator")

    srt_file = st.file_uploader("Upload .srt file", type=".srt")
    if srt_file:
        target_language = st.selectbox("Select Target Language", ["en", "fr", "ml", "es"])  # Add more language options if needed
        api_key = st.text_input("Enter API Key")

        if st.button("Translate"):
            with st.spinner("Translating..."):
                translated_file, translated_path = translate_srt(srt_file, target_language, api_key)
                st.success("Translation completed!")

            download_link = generate_download_link(translated_path, translated_file)
            st.markdown(download_link, unsafe_allow_html=True)

    random_celeb()

def generate_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()
    href = f'<a href="data:file/srt;base64,{encoded_file}" download="{file_name}">Download Translated File</a>'
    return href

if __name__ == '__main__':
    main()
