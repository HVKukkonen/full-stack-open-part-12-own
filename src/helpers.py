import json
from importlib import resources


# helper function to be called from here only
def write_config(dct):
    with open('config.txt', 'w') as f:
        f.write(json.dumps(dct))


def read_config():
    """Returns the configuration parameters as a dictionary"""
    with resources.open_text('data', 'config.txt') as f:
        return json.loads(f.read())


config = read_config()
