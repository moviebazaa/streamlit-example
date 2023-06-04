import streamlit as st
from pytube import YouTube

def download_video(url, output_path, resolution):
    try:
        # Create a YouTube object
        video = YouTube(url)

        # Get the stream with the selected resolution
        stream = video.streams.get_by_resolution(resolution)

        # Download the video
        stream.download(output_path)

        st.success("Video downloaded successfully!")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("YouTube Video Downloader")

    # Input fields
    video_url = st.text_input("Enter YouTube video URL:")
    output_directory = st.text_input("Enter output directory path:")

    # Quality selection
    available_qualities = ["1080p", "720p", "480p", "360p", "240p", "144p"]
    selected_quality = st.selectbox("Select video quality:", available_qualities)

    # Download button
    if st.button("Download"):
        if video_url and output_directory:
            download_video(video_url, output_directory, selected_quality)
        else:
            st.warning("Please enter the video URL and output directory path.")

if __name__ == "__main__":
    main()
