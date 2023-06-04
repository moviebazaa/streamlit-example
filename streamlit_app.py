import random
import streamlit as st
from pytube import YouTube
import moviepy.editor as mp

# Function for some random animations
def random_celeb():
    return random.choice([st.balloons()])

# Function to download YouTube videos in MP3 format
def download_mp3(url):
    video_caller = YouTube(url)
    st.info(video_caller.title, icon="ℹ️")

    # Get the highest quality audio stream
    audio_stream = video_caller.streams.filter(only_audio=True).order_by('abr').desc().first()

    if audio_stream is not None:
        # Download the audio stream
        audio_stream.download()

        # Convert the downloaded video to MP3
        video_filename = audio_stream.default_filename
        mp3_filename = video_filename.split('.')[0] + '.mp3'
        video_clip = mp.VideoFileClip(video_filename)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3_filename)
        audio_clip.close()
        video_clip.close()

        # Retrieve video metadata including frame rate
        video_metadata = mp.VideoFileClip(video_filename)
        frame_rate = video_metadata.fps

        st.success(f'Done! Frame rate: {frame_rate}')
        with open(mp3_filename, 'rb') as file:
            st.download_button(label='Download MP3', data=file, file_name=mp3_filename)
    else:
        st.error('Oops! Audio stream is not available!')

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
