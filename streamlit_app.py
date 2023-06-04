import random
import streamlit as st
import youtube_dl

# Function for some random animations
def random_celeb():
    return random.choice([st.balloons()])

# Function to download YouTube videos in MP3 format
def download_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'Untitled')
        st.info(video_title, icon="ℹ️")

        try:
            ydl.download([url])
            mp3_filename = f"{video_title}.mp3"

            st.success('Done!')
            with open(mp3_filename, 'rb') as file:
                st.download_button(label='Download MP3', data=file, file_name=mp3_filename)
        except Exception as e:
            st.error(f'Oops! An error occurred while downloading: {str(e)}')

# Integration of all above-defined functions
st.title("YouTube MP3 Downloader")
url = st.text_input(label="Paste your YouTube URL")
if st.button("Download"):
    if url:
        try:
            with st.spinner("Loading..."):
                download_mp3(url)
            random_celeb()
        except Exception as e:
            st.error(e)
