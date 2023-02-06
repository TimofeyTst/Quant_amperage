from django.http import HttpResponse
from django.shortcuts import render

device = {'name':'none',
          'status': 'nones'}

def index(request):
    return render(request, 'app/index.html', {'device': device})