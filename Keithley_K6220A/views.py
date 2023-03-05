from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import sleep
from .k6220 import *
from app.utils import formatValue

k6220 = None

def connect_device():
    global k6220
    try:
        return k6220.query('*IDN?') == 'KEITHLEY INSTRUMENTS INC.,MODEL 6221,4358011,D03  /700x '
    except Exception as e:
        return 0


    
# Должен сразу проверять подключение и узнавать текущее значение
def index(request):
    global k6220
    if k6220 is None:
        try:
            k6220 = K6220('GPIB0::12::INSTR')
        except Exception as e:
            yoko = None


    if k6220 and connect_device():
        device = { 'name': 'Keithley_K6220A',
                'name_replace': 'Keithley K6220A',
                'status': 'connected',
                'current_on': 1 if k6220.query("OUTPut?") == "1" else 0,
                'value': formatValue(k6220.get_current()),
                'amper_value': formatValue(k6220.get_current())[:-2],
                'volt_value': k6220.get_compliance(),
                'unit_a': formatValue(k6220.get_current())[-2:],
                'unit_v': 'V',
            }
    else:
        k6220 = None
        # Здесь по плану k6220 обнулился после выключения
        device = { 'name': 'Keithley_K6220A',
                'name_replace': 'Keithley K6220A',
                'status': 'disconnected',
                'current_on': 0,
                'value': '--- --',
                'amper_value': '0',
                'volt_value': '0',
                'unit_a': 'mA',
                'unit_v': 'V',
            }
        
    return render(request, 'Keithley_K6220A/index.html', {'device': device})


# Должен подключать ток и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        global k6220
        if k6220 and connect_device():
            if k6220.query("OUTPut?") == "1":
                k6220.output_off()
            else:
                k6220.output_on()

        return redirect('/Keithley_K6220A/')

            


def update_a(request):
     if request.method == 'POST':
        global k6220
        if k6220 and connect_device():
            units = {
                "mA":"e-3",
                "uA":"e-6",
            }
            ampers = float(request.POST['ampers'] + units[request.POST['ampers_type']])
            k6220.set_current(ampers)

        return redirect(request.META.get('HTTP_REFERER', '/'))
     
def update_v(request):
     if request.method == 'POST':
        global k6220
        if k6220 and connect_device():
            volts = 0 if request.POST['volts'] == '' else float(request.POST['volts'])
            k6220.set_compliance(volts)

        return redirect(request.META.get('HTTP_REFERER', '/'))