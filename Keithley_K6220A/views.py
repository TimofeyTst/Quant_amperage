from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import sleep
# from .k6220 import *


def set_value():
    # value = k6220.get_current()
    value = 6e-6 # Commit this
    if abs(value) >= 1e-3:
        suffix = "mA"
        factor = 1e3
    else:
        suffix = "uA"
        factor = 1e6
    print("factor =", factor, "suffix =", suffix, "value =", value)
    return "{:.2f}{}".format(value * factor, suffix)


def is_current_on():
    # if k6220.query("OUTPut?") == "1":
    #     return 1
    # else:
    #     return 0
    return True

def is_connect():
    # if k6220.query('*IDN?') == 'KEITHLEY INSTRUMENTS INC.,MODEL 6221,4358011,D03  /700x ':
    #     return 1
    # else:
    #     return 0
    return True


# k6220 = K6220('GPIB0::12::INSTR')
device = { 'name':'Keithley_K6220A',
            'name_replace': 'Keithley K6220A',
            'status': 'disconnected',
            'connected': is_current_on(),
            'value': set_value(),
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


    
# Должен сразу проверять подключение и узнавать текущее значение
def index(request):
    if is_current_on() == 1:
        # device['volt_value'] = k6220.get_compliance()
        device['volt_value'] = 9.0 # Comment this
        device['value'] = set_value()
        device['amper_value'] =  device['value'][:-2]
    
    if is_connect():
        device['status'] = 'connected'
    else:
        device['status'] = 'disconnected'
        
    return render(request, 'Keithley_K6220A/index.html', {'device': device})


# Должен подключать и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        if is_current_on() == 1:
            print("Is_connect = 1 from connect")
            # k6220.output_off()
            device['connected'] = 0
            device['status'] = 'disconnected'
        else:
            # k6220.output_on()
            device['connected'] = 1
            device['status'] = 'connected'

        context = {
            'device': device, 
        }
        return redirect('/' + str(device['name']) + '/', context=context)
            


def update_a(request):
     if request.method == 'POST' and is_connect() == 1:
        ampers = float(request.POST['ampers'] + units[request.POST['ampers_type']])
        # k6220.set_current(ampers)
        device['amper_value'] = request.POST['ampers']
        device['unit_a'] = request.POST['ampers_type']
        device['value'] = set_value()

        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
     
def update_v(request):
     if request.method == 'POST' and is_connect() == 1:
        volts = 0 if request.POST['volts'] == '' else float(request.POST['volts'])
        
        # k6220.set_compliance(volts)
        device['volt_value'] = request.POST['volts']
        device['unit_v'] = request.POST['volts_type']

        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)