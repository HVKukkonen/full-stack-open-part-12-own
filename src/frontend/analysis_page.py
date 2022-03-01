from dash import Dash, dcc, html, Input, Output
from django_plotly_dash import DjangoDash
import requests
import sounddevice as sd
import json
import os, sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, src_dir)
# own modules
from frontend.sound_stream import sound_stream

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
        
        return 'Rec stream start'


@app.callback(
    Output('temp', 'children'),
    Input('record-stop', 'n_clicks')
)
def stop(n_clicks):
    if n_clicks:
        sound_stream.close()
        sound_stream.stop()

        return 'Stopped'
    