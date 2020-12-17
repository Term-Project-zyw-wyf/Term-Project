#!/usr/bin/env python
# encoding: utf-8
from google.cloud import speech_v1p1beta1 as speech
import os
import sys
import wave
from pydub import AudioSegment
import math

client = speech.SpeechClient()

o_file = str(sys.argv[1])


with wave.open(o_file, "rb") as wave_file:
    frame_rate = wave_file.getframerate()
    num_channel = wave_file.getnchannels()
print(frame_rate)
print(num_channel)

if num_channel > 1:
    sound = AudioSegment.from_wav(o_file)
    sound = sound.set_channels(1)
    sound.export("new" + o_file + ".wav", format="wav")
    speech_file = "new" + o_file + ".wav"
else:
    speech_file = o_file

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz = frame_rate,
    language_code="en-US",
    enable_speaker_diarization=True,
    #diarization_speaker_count=2,
)

operation = client.long_running_recognize(config=config, audio=audio)

print("Waiting for operation to complete...")
response = operation.result(timeout=90)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

# Printing out the output:
#for word_info in words_info:
 #   print(
   #     u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
   # )

speaker_tag = 0
for word_info in words_info:
    if speaker_tag == word_info.speaker_tag:
        print(word_info.word, end=" ")
    else:
        print("\n")
        print(word_info.speaker_tag)
        print(word_info.word, end=" ")
    speaker_tag = word_info.speaker_tag
