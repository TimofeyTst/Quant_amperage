from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import sleep
from .Yokogawa_GS200 import *

yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')

def set_value():
    value = yoko.get_current()
    if abs(value) >= 1e-3:
        suffix = "mA"
        factor = 1e3
    else:
        suffix = "uA"
        factor = 1e6
    print("factor =", factor, "suffix =", suffix, "value =", value)
    return "{:.2f}{}".format(value * factor, suffix)


def is_current_on():
    return yoko.get_status()


def is_connect():
    if yoko.get_id() == 'YOKOGAWA,GS211,91VB13481,2.02\n':
        return 1
    else:
        return 0


device = { 'name':'Yokogawa_GS210',
            'name_replace': 'Yokogawa GS210',
            'status': 'connected' if is_connect() else 'disconnected',
            'current_on': is_current_on() if is_connect() else 'disconnected',
            'value': set_value() if is_connect() else '--- --',
            'amper_value': '0',
            'volt_value': yoko.get_voltage_compliance() if is_connect() else '0',
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
    if is_connect():
        if is_current_on() == 1:
            device['volt_value'] = yoko.get_voltage_compliance()
            device['value'] = set_value()
            device['amper_value'] =  device['value'][:-2]
        
    return render(request, 'Yokogawa_GS210/index.html', {'device': device})


# Должен подключать и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        if is_connect():
            if is_current_on() == 1:
                yoko.set_status(0)
                device['current_on'] = 0
            else:
                yoko.set_status(1)
                device['current_on'] = 1

        context = {
            'device': device, 
        }
        return redirect('/' + str(device['name']) + '/', context=context)
            


def update_a(request):
     if request.method == 'POST':
        if is_connect():
            ampers = float(request.POST['ampers'] + units[request.POST['ampers_type']])
            yoko.set_current(ampers)
            device['amper_value'] = request.POST['ampers']
            device['unit_a'] = request.POST['ampers_type']
            device['value'] = set_value()

        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
     
def update_v(request):
     if request.method == 'POST':
        if is_connect():
            volts = 0 if request.POST['volts'] == '' else float(request.POST['volts'])
            
            yoko.set_voltage_compliance(volts)
            device['volt_value'] = request.POST['volts']
            device['unit_v'] = request.POST['volts_type']

        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)