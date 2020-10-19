import speech_recognition as sr
import pyaudio

def audio_recognition():
    r = sr.Recognizer()
    with sr.WavFile("mc3.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        print("Transcription: " + r.recognize_google(audio))   # recognize speech using Google Speech Recognition
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")

                                               # NOTE: this requires PyAudio because it uses the Microphone class
def stream_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

    try:
        print("You said " + r.recognize_google(audio))    # recognize speech using Google Speech Recognition
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")


if __name__ == "__main__":
    audio_recognition()
    stream_recognition()