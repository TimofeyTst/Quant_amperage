from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import sleep
# from .k6220 import *

device = { 'name':'Yokogawa_GS210',
            'name_replace': 'Yokogawa GS210',
            'status': 'disconnected',
            'value': '--- --',
            'amper_value': '0',
            'volt_value': '0',
            'unit_a': 'mA',
            'unit_v': 'V',
        }

units = {
    "mA":"e-3",
    "uA":"e-6",
    "V":"e-0",
    "mV":"e-3",
}

def is_connect():
    # return (k6220.query("OUTPut?"))
    return "1"

def set_value():
    # device['value'] = k6220.query("CURRent?") + "A" 
    device['value'] = ("CURRent?") + "A" 
    
# Должен сразу проверять подключение и узнавать текущее значение
def index(request):
    if is_connect() == "1":
        # print("COMpilance = ", k6220.get_compliance())
        device['status'] = 'connected'
        set_value()
    else:
        device['status'] = 'disconnected'
        device['value'] = '--- --'
    return render(request, 'Yokogawa_GS210/index.html', {'device': device})


# Должен подключать и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        if is_connect() == '1':
            # k6220.output_off()
            device['status'] = 'disconnected' # Must be connecting
            device['value'] = '--- --' # clear
        else:
            # k6220.output_on()
            device['status'] = 'connected' # Must be connecting

        device['amper_value'] = '0' # clear
        device['volt_value'] = '0' # clear
        context = {
            'device': device, 
        }
        return redirect('/' + str(device['name']) + '/', context=context)
            


def update_a(request):
     if request.method == 'POST' and is_connect() == "1":
        ampers = f"CURRent {request.POST['ampers']}{units[request.POST['ampers_type']]}"
        # k6220.write(ampers)
        device['amper_value'] = request.POST['ampers']
        device['unit_a'] = request.POST['ampers_type']

        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
     
def update_v(request):
     if request.method == 'POST' and is_connect() == "1":
        # volts = f"CURRent {request.POST['volts']}{units[request.POST['volts_type']]}" #not important
        volts = 0 if request.POST['volts'] == '' else float(request.POST['volts'])
        
        print("volts = ", volts)
        # k6220.set_compliance(volts)
        device['volt_value'] = request.POST['volts']
        device['unit_v'] = request.POST['volts_type']


        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)