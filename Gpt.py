import json
from openai import AzureOpenAI
import streamlit as st


GPT4o_API_KEY = st.secrets.azure_keys["GPT4o_API_KEY"]
GPT4o_DEPLOYMENT_ENDPOINT = st.secrets.azure_keys["GPT4o_DEPLOYMENT_ENDPOINT"]
GPT4o_DEPLOYMENT_NAME = st.secrets.azure_keys["GPT4o_DEPLOYMENT_NAME"]
GPT4o_API_VERSION = st.secrets.azure_keys["GPT4o_API_VERSION"]
MODEL = "gpt-4o" 

AzureClient = AzureOpenAI(
  azure_endpoint = GPT4o_DEPLOYMENT_ENDPOINT,
  api_key=GPT4o_API_KEY,
  #api_version="2024-02-01"
  azure_deployment= GPT4o_DEPLOYMENT_NAME,
  api_version=GPT4o_API_VERSION,
)

def removeUtterance(my_audio_chunks):
    #print("remove utterances",my_audio_chunks)

    new_audio_chunks = my_audio_chunks

    for data in new_audio_chunks:
        data["chunk"] = ""

    completion = AzureClient.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},
    messages=[
    {"role": "system", "content": "You are a trainer who always responds in JSON"},
    {"role": "user", "content": json.dumps(new_audio_chunks)+ "remove hmm & umm from transcription key and return data in same format"}
    ])

    content=json.loads(completion.choices[0].message.content)

    for transcriptions in content.values():
        data = transcriptions
    

    for i in range(0,len(my_audio_chunks)):
         my_audio_chunks[i]["transcription"]= data[i]['transcription']
    
