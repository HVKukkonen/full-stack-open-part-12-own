from dash import Dash, dcc, html, Input, Output
from django_plotly_dash import DjangoDash
import requests
import sounddevice as sd
# own modules
from sound_stream import sound_stream

app = DjangoDash('analysisPage')

app.layout = html.Div([
    html.H2('Dash: Speech analysis'),
    html.Button('Record', id='record-start'),
    html.Button('Stop', id='record-stop'),
    html.Div([
        html.Div(id='temp'),
        html.Div(id='temp2'),
        html.Div(id='pronunciation')
    ])
])


# TODO start recording speech
@app.callback(
    Output('temp2', 'children'),
    Input('record-start', 'n_clicks')
)
def record(n_clicks):
    # skip when initialised
    if n_clicks:
        sound_stream.start()
        # fs = 44100  # Sample rate
        # seconds = 1  # Duration of recording
        # test_rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        # sd.wait()
        # print('test_rec has', test_rec )
        return 'Rec stream start'


@app.callback(
    Output('temp', 'children'),
    Input('record-stop', 'n_clicks')
)
def stop(n_clicks):
    if n_clicks:

        print('available', sound_stream.read_available)
        speech_data = sound_stream.read(100)
        print('sound_stream passed at stop', speech_data)
        # print('sound_stream passed at stop has something', (speech_data > 0).any())

        sound_stream.stop()

        # FIXME modify routing when in production 
        backend_url = 'http://localhost:8000/'
        session = requests.Session()
        # retrieve the csrf cookie
        session.get(backend_url)
        if 'csrftoken' in session.cookies:
            csrftoken = session.cookies['csrftoken']
        # pass to the speech model to determine whether the pronunciation was correct
        # the session with the cookie acquired in GET needs to be used
        # {'csrfmiddlewaretoken': csrftoken} can also be passed along the data
        res = session.post(backend_url, headers={'X-CSRFToken': csrftoken}, data={'speech_data': speech_data})

        return 'Response status was: {}'.format(str(res.status_code))
    