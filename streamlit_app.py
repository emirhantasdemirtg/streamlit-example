!pip install streamlit torch numpy scipy soundfile ffmpeg-python PySoundFile tqdm yt-dlp git+https://github.com/facebookresearch/demucs#egg=demucs

import io
from pathlib import Path
import subprocess as sp
import sys
from typing import Dict, Tuple, Optional, IO
import zipfile
import os
import streamlit as st
import yt_dlp

def download_audio():
    url = st.text_input("Enter a YouTube URL to download audio from:")
    if st.button("Download"):
        # Download audio from the entered URL and save to the input directory
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(in_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320'
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        st.success("Audio downloaded.")

def separate_audio():
    if st.button("Separate"):
        separate()
        st.success("Audio separated.")
        
        
def main():
    st.title("Audio Separator")

    # Define the input and output paths
    in_path = Path(st.text_input("Input directory:", "/content/demucs"))
    out_path = Path(st.text_input("Output directory:", "/content/demucs_separated"))

    # Define the model and output options
    model = st.selectbox("Model:", ["htdemucs_ft"])
    extensions = ["mp3", "wav", "ogg", "flac"]
    two_stems = None
    mp3 = st.checkbox("Output as MP3", value=True)
    if mp3:
        mp3_rate = st.slider("MP3 bitrate:", 64, 320, 320)
        float32 = False
        int24 = False
    else:
        float32 = st.checkbox("Output as float32 WAV")
        int24 = st.checkbox("Output as int24 WAV")
        mp3_rate = None
    if st.checkbox("Separate only one stem"):
        two_stems = st.selectbox("Select stem to separate:", ["vocals", "drums", "bass", "other"])

    # Define the buttons for downloading and separating audio
    st.write("")
    col1, col2 = st.beta_columns(2)
    with col1:
        download_audio()
    with col2:
        separate_audio()

    # Show the list of files in the input and output directories
    st.write("")
    st.subheader("Files")
    st.write("Input directory:")
    input_files = [f.name for f in in_path.glob("*") if f.suffix.lstrip(".") in extensions]
    if input_files:
        st.write("\n".join(input_files))
    else:
        st.write("No audio files found in input directory.")
    st.write("Output directory:")
    output_files = [f.name for f in out_path.glob("*") if f.suffix.lstrip(".") in extensions]
    if output_files:
        st.write("\n".join(output_files))
    else:
        st.write("No audio files found in output directory.")

if __name__ == "__main__":
    main()       
        
