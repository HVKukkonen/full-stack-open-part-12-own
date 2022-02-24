from django import conf
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import os
import sys
import numpy as np

# own imports
from . import speech_model
# append parallel folder to sys path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
# registration code needs to be in a location that will be imported into the Django process
# before any model or template tag attempts to use it
from django_plotly_dash.templatetags import plotly_dash
from frontend.analysis_page import app
from helpers import config

# creates the csrf cookie event though csrf_cookie template tag is not used
@ensure_csrf_cookie
def analysis(request):
    """View function for the analysis"""

    # dict to be passed to the template
    context = {}

    if request.method == 'POST':
        # TODO: get speech.wav from request
        speech = request.POST.getlist('speech_data')
        speech = np.array(speech).reshape((-1, config['channels']))

        # boolean whether the pronunciation was correct
        context['syllable_correct'] = speech_model.pronounced_correct(speech)

    return render(request, 'analysis_page.html', context=context)
