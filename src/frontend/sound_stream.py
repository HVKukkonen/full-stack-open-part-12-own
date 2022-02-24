import sounddevice as sd
import numpy as np

# own modules
from helpers import config


class SpeechStream(sd.InputStream):
    def __init__(self, samplerate=None, blocksize=None, device=None, channels=None, dtype=None, latency=None, extra_settings=None, callback=None, finished_callback=None, clip_off=None, dither_off=None, never_drop_input=None, prime_output_buffers_using_stream_callback=None):
        super().__init__(samplerate, blocksize, device, channels, dtype, latency, extra_settings, callback, finished_callback, clip_off, dither_off, never_drop_input, prime_output_buffers_using_stream_callback)
    
        self.input_buffer = np.array()

    def insert_buffer(self, arr):
        self.input_buffer = np.concatenate([self.input_buffer, arr])


def callback(indata, frames, time, status):
    pass


# create the input sound stream instance
sound_stream = SpeechStream(
    samplerate=config['sample_rate'],
    channels=config['channels']
)
