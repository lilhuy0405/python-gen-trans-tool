# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys
import shutil

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 milliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="fr-FR")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text + "\n"
    # return the text for all chunks detected
    return whole_text

# path = "input-wav.wav"
# print("\nFull text:", get_large_audio_transcription(path))

def convert_to_wav(path): 
    # files                                                                         
    src = path
    dst = "input.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    return dst

def remove_file(path):
    if os.path.exists(path):
       os.remove(path)
    else:
        print("The file does not exist")
    
def remove_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        print("The directory does not exist")

def clean_up():
    remove_file(sys.argv[1])
    remove_file("input.wav")
    remove_directory("audio-chunks")

def main():
    path = sys.argv[1]
    if(".mp3" in path): 
        print("Converting files to wav format...")
        path = convert_to_wav(path)
    print("\nAudio Recognize process begin.....")
    print("\nFull text:", get_large_audio_transcription(path))
    print("cleaning up...")
    print("all done...")
    clean_up()
    
main()