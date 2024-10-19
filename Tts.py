import tempfile 
from google.cloud import texttospeech
from google.oauth2 import service_account
import os 
import json
import streamlit as st
import toml
#from streamlit-app import getCredentials

#client_file = './assets/speech.json'


#config =toml.load('service_account.toml')
service_account_info = st.secrets.service_account
credentials = service_account.Credentials.from_service_account_info(service_account_info)
client = texttospeech.TextToSpeechClient(credentials=credentials)

def tts(data):
    text_block = data["transcription"]
    synthesis_input = texttospeech.SynthesisInput(text = text_block)

    voice = texttospeech.VoiceSelectionParams(
        language_code = "en-US",
        name = "en-US-Studio-O"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3,
        effects_profile_id = ['small-bluetooth-speaker-class-device'],
        speaking_rate= 1 ,
        pitch=1
    )

    responses = client.synthesize_speech(
        input = synthesis_input,
        voice = voice ,
        audio_config = audio_config
    )
  
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file_path = temp_audio_file.name

        temp_audio_file.write(responses.audio_content)
        data["file"] = temp_audio_file_path

def textToSpeech(my_audio_chunks):
    for data in my_audio_chunks:
        tts(data)