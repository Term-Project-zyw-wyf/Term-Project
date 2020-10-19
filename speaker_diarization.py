from google.cloud import speech_v1p1beta1 as speech
import speech_recognition as sr
import pyaudio

client = speech.SpeechClient()

speech_file = "test3.wav"
with open(speech_file, 'rb') as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)



config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-US',
    enable_speaker_diarization=True,
    diarization_speaker_count=4)

print('Waiting for operation to complete...')
response = client.recognize(config=config, audio=audio)
# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

# Printing out the output:
speaker_tag = 0
for word_info in words_info:
    if speaker_tag == word_info.speaker_tag:
        print(word_info.word, end=" ")
    else:
        print("\n")
        print(word_info.speaker_tag)
        print(word_info.word, end=" ")
    speaker_tag = word_info.speaker_tag