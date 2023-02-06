from django.http import HttpResponse
from django.shortcuts import render

device = {'name':'Keithley_K6220A',
          'status': 'Connected'}

def index(request):
    return render(request, 'Keithley_K6220A/index.html', {
        'device':device
        })