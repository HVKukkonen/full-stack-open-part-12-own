import sounddevice as sd
import numpy as np
import queue
import requests
import threading

# own modules
from helpers import config


def callback(target):
    def prepped_callback(indata, frames, time, status):
        if status:
            print(status)

        target.put(indata)

    return prepped_callback
        

def final_call(target):
    def prepped_callback():
        speech_data = []

        def worker():
            while True:
                # get item from the queue, raises Empty when queue emptied
                item = target.get()
                speech_data.append(item)
                # inform the queue the item has been processed
                target.task_done()

        # process queue items into np.array
        threading.Thread(target=worker, daemon=True).start()
        speech_data = np.concatenate(speech_data)

        # FIXME modify routing when in production 
        backend_url = 'http://localhost:8000/analyser/'
        session = requests.Session()
        # retrieve the csrf cookie
        session.get(backend_url)
        if 'csrftoken' in session.cookies:
            csrftoken = session.cookies['csrftoken']
        # pass to the speech model to determine whether the pronunciation was correct
        payload = {'speech_data': speech_data.tolist()}
        # the session with the cookie acquired in GET needs to be used
        # {'csrfmiddlewaretoken': csrftoken} can also be passed along the data
        res = session.post(backend_url, headers={'X-CSRFToken': csrftoken}, data=payload)
        # TODO handle HTTP errors

    return prepped_callback


# queue to receive input
speech_queue = queue.Queue()

# create the input sound stream instance
sound_stream = sd.InputStream(
    samplerate=config['sample_rate'],
    channels=config['channels'],
    callback=callback(speech_queue),
    finished_callback=final_call(speech_queue)
)
