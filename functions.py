from pydub import AudioSegment
import tempfile

def combinedAudio(my_audio_chunks):
  

  # Load the first audio file
  combined_audio = AudioSegment.from_file(my_audio_chunks[0]["file_with_silence"])

  # Loop through the rest of the audio file_with_silencefiles and append them to the first
  for data in my_audio_chunks[1:]:
    current_audio = AudioSegment.from_file(data["file_with_silence"])
    combined_audio += current_audio

  # Export the combined audio as a single file
  output_file = "combined_audio.mp3"
  combined_audio.export(output_file, format="mp3")

  print("combined length",len(combined_audio))
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
      temp_audio_file_path = temp_audio_file.name
      combined_audio.export(temp_audio_file_path, format="mp3")
  
  print("Audio files combined successfully!")
  return temp_audio_file_path

def fillAudioWithNoise(my_audio_chunks):
    for data in my_audio_chunks:
        generateAudioWithSilence(data)

def generateAudioWithSilence(data):
  #print(data)
    audio_file_path = data["file"]
    print(data)
    try:
        audio = AudioSegment.from_file(audio_file_path)
    except:
        audio = generate_silence(1)
    #print(len(audio))

    silence = generate_silence(data["end_time"]-data["start_time"]-len(audio))

  

    audio_with_silence =  audio + silence 
    print(audio_file_path,len(audio),len(silence),len(audio_with_silence))
  # Add silence at the end of the audio
  # audio_with_silence = audio + silence

  # Export the new audio with silence
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file_path = temp_audio_file.name
        audio_with_silence.export(temp_audio_file_path, format="mp3")
        
        data["file_with_silence"] = temp_audio_file_path
  #output_file_path = "audio_with_silence.mp3"
  #audio_with_silence.export(output_file_path, format="mp3")

    print("Audio file with silence added successfully!")

def generate_silence(duration_ms):
    # Generate silence of given duration in milliseconds
    return AudioSegment.silent(duration=duration_ms)

def adjustTranscription(my_audio_chunks):
  for i in range(0,len(my_audio_chunks)):
    if(i==len(my_audio_chunks)-1):
      break;

    data = my_audio_chunks[i]
    
    no_of_words=len(data["transcription"].split(" "))
    max_audio_length=(data["end_time"]-data["start_time"])/1000
    # 1 sec = 2.5 words 
    max_words_permitted = max_audio_length*3
    if(no_of_words>max_words_permitted):
      list_of_allowed_words = data["transcription"].split(" ")[:int(max_words_permitted)]
      data["transcription"] = " ".join(list_of_allowed_words)
      list_of_extra_words = data["transcription"].split(" ")[int(max_words_permitted):]
      print(" ".join(list_of_extra_words))
      my_audio_chunks[i+1]["transcription"] = " ".join(list_of_extra_words)+" "+my_audio_chunks[i+1]["transcription"]
      #data["transcription"]=" ".join(data["transcription"].split(" ")[:int(max_words_permitted)])    