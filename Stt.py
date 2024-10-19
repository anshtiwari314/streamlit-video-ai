from pydub import AudioSegment
import math 
from google.cloud import texttospeech, speech
import tempfile 
import io
from google.oauth2 import service_account
import os 
import json
import toml 
import streamlit as st
#from streamlit-app import getCredentials

#client_file = './assets/speech.json'


#config =toml.load('service_account.toml')
service_account_info = st.secrets.service_account
credentials = service_account.Credentials.from_service_account_info(service_account_info)

sttClient = speech.SpeechClient(credentials=credentials)

def speechToText(audio_file_name,my_audio_chunks):
    print("inside stt",audio_file_name)
    audio = AudioSegment.from_file(audio_file_name)
    chunk_length_ms = 3000
    audio_length = len(audio)

    num_chunks = math.ceil(audio_length / chunk_length_ms)

    count = 0
    my_audio_chunks.clear()

    for i in range(num_chunks):
        start_time = i * chunk_length_ms
        end_time = start_time + chunk_length_ms

        if end_time > audio_length:
            end_time = audio_length

        chunk = audio[start_time:end_time]
        temp_dict = {"chunk":"","transcription":"","start_time":start_time,"end_time":end_time,"file":"","file_with_silence":""}
        temp_dict["chunk"]=chunk

        my_audio_chunks.append(temp_dict)
        count= count+1
        print(count)

        config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz = 44100,
        language_code='en-US'
        )

    print("inside stt1",my_audio_chunks)
    #new_audio_chunks = my_audio_chunks[:2]

    for data in my_audio_chunks:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            data["chunk"].export(tmpfile.name, format="mp3")

            with io.open(tmpfile.name,'rb') as f:
                content = f.read()
                my_audio = speech.RecognitionAudio(content = content)

                response=sttClient.recognize(config=config,audio=my_audio)
                print(response)
                try:
                    data["transcription"] = response.results[0].alternatives[0].transcript
                except:
                    data["transcription"] = ""


    #print("stt2",new_audio_chunks)
    return my_audio_chunks
    