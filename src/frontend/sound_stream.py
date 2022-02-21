import sounddevice as sd

# create the input sound stream instance
sound_stream = sd.InputStream(samplerate=44100, channels=2)
