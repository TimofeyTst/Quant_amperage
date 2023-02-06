from django.http import HttpResponse
from django.shortcuts import render

device = { 'name':'Not selected',
            'status': 'disconnected',
            'value': '--- --',
            'amper_value': '0',
            'volt_value': '0',
        }

def index(request):
    return render(request, 'app/index.html', {'device': device})