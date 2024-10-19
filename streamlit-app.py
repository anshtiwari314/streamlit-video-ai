import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
import tempfile
from pydub import AudioSegment
import os
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import texttospeech, speech
import io
from dotenv import load_dotenv
from Stt import speechToText
from Gpt import removeUtterance
from Tts import textToSpeech
from functions import combinedAudio, fillAudioWithNoise, adjustTranscription
import math 
import time 
import json 
import toml

my_audio_chunks = []


load_dotenv()

#client_file = './assets/speech.json'
#print(json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')))

#credentials = service_account.Credentials.from_service_account_file(client_file)

#config =toml.load('service_account.toml')
#service_account_info = config['service_account']

service_account_info = st.secrets.service_account

#service_account_info = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
credentials = service_account.Credentials.from_service_account_info(service_account_info)

mp3_file = "audio.mp3"

# video_file = open("videoplayback.mp4", "rb")
# video_bytes = video_file.read()


    


uploaded_file = st.file_uploader("Choose a file",type=["mp4"])
#uploaded_file = None

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    

    ## 
    st.write("audio extraction begins...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
      temp_video_file.write(uploaded_file.getbuffer())  
      temp_video_path = temp_video_file.name

    #print("video",video_file,"uploaded",uploaded_file.name)
      video_clip = VideoFileClip(temp_video_path)
      audio_clip = video_clip.audio

    
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_aud_file:
      temp_audio_file_path = temp_aud_file.name 
      
    audio_clip.write_audiofile(temp_audio_file_path)
    print(temp_audio_file_path)  
    
    st.write("speech to text conversion begins...")
    ## use this audio file for speech to text 
    my_audio_chunks=speechToText(temp_audio_file_path,my_audio_chunks)
    #print("after stt",my_audio_chunks)
    
    st.write("removing utterances begins...")
    ## use gpt 4-o to remove utterance 
    removeUtterance(my_audio_chunks)  
    print("after gpt 4",my_audio_chunks)

    st.write("text adjustment as per rate of speech begins ...")
    adjustTranscription(my_audio_chunks)
    print("text adjustment",my_audio_chunks)

    st.write("text to speech conversion begins...")
    textToSpeech(my_audio_chunks)
    #print("after tts",my_audio_chunks)

    st.write("filling empty audio with silent noise...")
    fillAudioWithNoise(my_audio_chunks)
    #print("after filling noise",my_audio_chunks)

    st.write("combining audio files...")
    processed_aud_file=combinedAudio(my_audio_chunks)
    #print(my_audio_chunks)


    st.write("replacing audio with old one...")
    # video (no audio)
    clip_without_audio=video_clip.without_audio()
    # only audio 
    custom_audio_clip = AudioFileClip(processed_aud_file)
    
    # after combining above files
    clip_replaced_audio=clip_without_audio.set_audio(custom_audio_clip)

    # creating a temp file in memory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file2:
      clip_replaced_audio.write_videofile(temp_video_file2.name,codec='libx264')

      with open(temp_video_file2.name, 'rb') as video_file:
        byte = video_file.read()
        buffer = io.BytesIO(byte)

    st.write("video loading...")
    st.video(buffer)
    

    


    


