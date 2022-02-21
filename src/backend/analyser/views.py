from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
# own imports
from . import speech_model
# append parallel folder to sys path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
# registration code needs to be in a location that will be imported into the Django process
# before any model or template tag attempts to use it
from frontend.analysis_page import app
from django_plotly_dash.templatetags import plotly_dash

# creates the csrf cookie event though csrf_cookie template tag is not used
@ensure_csrf_cookie
def analysis(request):
  """View function for the analysis"""

  # TODO: get speech.wav from request
  speech = request.POST
  print('post params at view', speech)

  # dict to be passed to the template 
  context = {
    # boolean whether the pronunciation was correct 
    'syllable_correct': speech_model.pronounced_correct(speech)
  }

  return render(request, 'analysis_page.html', context=context)

