from django.http import HttpResponse
from django.shortcuts import render

device = { 'name':'Not selected',
            'name_replace': 'Not selected',
            'status': 'disconnected',
            'current_on': 0,
            'value': '--- --',
            'amper_value': '0',
            'volt_value': '0',
            'unit_a': 'mA',
            'unit_v': 'V',
        }

def index(request):
    return render(request, 'app/index.html', {'device': device})