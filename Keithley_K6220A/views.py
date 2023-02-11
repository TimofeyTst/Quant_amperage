from django.http import HttpResponse
from django.shortcuts import render, redirect
# from  drivers import instr
from time import sleep
# from .k6220 import *

device = { 'name':'Keithley_K6220A',
            'status': 'disconnected',
            'value': '--- --',
            'amper_value': '0',
            'volt_value': '0',
        }
# k6220 = K6220.new()

def is_connect():
    # return k6220.output_on()
    return True

# Должен сразу проверять подключение и узнавать текущее значение
def index(request):
    if is_connect:
        device['status'] = 'connected'
        # device['value'] = k6220.get_current() # узнавать текущее значение
        # device['value'] = 20.5 # узнавать текущее значение
    else:
        device['status'] = 'disconnected'
        device['value'] = '--- --'
    return render(request, 'Keithley_K6220A/index.html', {'device': device})


# Должен подключать и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        # k6220.output_on()
        device['status'] = 'connected' # Must be connecting
        # device['value'] = k6220.get_current() # узнавать текущее значение
        device['value'] = 15.62 # узнавать текущее значение
        device['amper_value'] = '0' # clear
        device['volt_value'] = '0' # clear
        context = {
            'device': device, 
        }
        return redirect('/' + str(device['name']) + '/', context=context)


def disconnect(request):
    if request.method == 'POST':
        device['status'] = 'disconnected' # Must be connecting
        device['value'] = '--- --' # clear
        device['amper_value'] = '0' # clear
        device['volt_value'] = '0' # clear
        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
    

def update_a(request):
     if request.method == 'POST':
        # k6220.set_current(request.POST['ampers'])
        # print(type(request.POST['ampers']))
        # device['value'] = k6220.get_current()
        device['value'] = request.POST['ampers'] + ' ' + request.POST['ampers_type']
        device['amper_value'] = 37.8

        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
     
def update_v(request):
     if request.method == 'POST':
        # k6220.set_compliance(request.POST['volts'])
        # device['value'] = k6220.get_current()
        device['value'] = request.POST['volts'] + ' ' + request.POST['volts_type']
        device['volt_value'] = request.POST['volts']
        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)